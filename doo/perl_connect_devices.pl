#!/usr/bin/env perl
use strict;
use warnings;
use YAML::XS 'LoadFile';
use Net::OpenSSH;
use Net::Telnet;

my $yaml_file = '~/sp-1/doo/configs.3/devices.yaml';  # Ensure this path is correct
my $data = LoadFile($yaml_file);

my @reachable;
my @unreachable;

print "\n--- CE Device Connection Script (Ping + SSH/Telnet) ---\n";

foreach my $device (@{$data->{devices}}) {
    my $name = $device->{name};
    my $ip   = $device->{hostname};
    my $user = $device->{username} || 'cisco';
    my $pass = $device->{password} || 'cisco';
    my $type = $device->{device_type};

    # Only handle CE devices
    next unless $name =~ /-CE-/i;

    print "\n[$name] Pinging $ip ... ";
    my $ping_result = system("ping -c 1 -W 2 $ip > /dev/null 2>&1");

    if ($ping_result == 0) {
        print "Reachable ✅\n";
        push @reachable, $name;

        if ($type eq 'cisco_xr') {
            print "[$name] Connecting via SSH...\n";
            my $ssh = Net::OpenSSH->new($ip, user => $user, password => $pass, timeout => 5);
            if ($ssh->error) {
                warn "SSH failed for $name: " . $ssh->error . "\n";
            } else {
                print $ssh->capture("show version | include IOS");
            }

        } elsif ($type eq 'cisco_ios') {
            print "[$name] Connecting via Telnet...\n";
            my $telnet = Net::Telnet->new(Host => $ip, Timeout => 5, Errmode => 'return');
            $telnet->open($ip);
            $telnet->waitfor('/Username:/i');
            $telnet->print($user);
            $telnet->waitfor('/Password:/i');
            $telnet->print($pass);
            my @output = $telnet->cmd('show version | include IOS');
            print @output;
            $telnet->close;
        } else {
            warn "Unknown device type for $name\n";
        }

    } else {
        print "Unreachable ❌\n";
        push @unreachable, $name;
    }
}

print "\n--- Summary ---\n";
print "Reachable CE Devices:\n  ", join("\n  ", @reachable), "\n" if @reachable;
print "Unreachable CE Devices:\n  ", join("\n  ", @unreachable), "\n" if @unreachable;
