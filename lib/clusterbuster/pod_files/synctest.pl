#!/usr/bin/perl

use POSIX;
use strict;
require "clientlib.pl";

my ($sync_count, $sync_cluster_count, $sync_sleep, $processes) = parse_command_line(@ARGV);
initialize_timing();

sub runit() {
    my ($data_start_time) = xtime();
    my ($ucpu0, $scpu0) = cputime();
    foreach my $i (1..$sync_count) {
	foreach my $j (1..$sync_cluster_count) {
	    sync_to_controller(idname($$, $i, $j));
	}
	if ($sync_sleep > 1) {
	    usleep($sync_sleep * 1000000);
	}
    }
    my ($ucpu1, $scpu1) = cputime();
    $ucpu1 -= $ucpu0;
    $scpu1 -= $scpu0;

    my ($data_end_time) = xtime();
    report_results($data_start_time, $data_end_time, $data_end_time - $data_start_time, $ucpu1, $scpu1);
}

run_workload(\&runit, $processes);
