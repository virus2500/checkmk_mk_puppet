## mk_puppet Plugin

This repository contains the 3.0 for checkmk 2.3.0p33+ and 2.4.0.

Based on the work of [DECOIT](https://github.com/decoit/check_mk/tree/main/mk_puppet) and
the mk_puppet plugin by [Alan Good](https://github.com/allangood/check_mk/tree/master/plugins/puppet)

Checks for puppet:
 - Puppet Agent Events Failure
 - Puppet Agent Last Run
 - Puppet Agent Resource Changed
 - Puppet Agent Resource Failed
 - Puppet Agent Resource Failed to Restart
 - Puppet Agent Resources Out Of Sync
 - Puppet Agent Resources Restarted
 - Puppet Agent Resources Scheduled
 - Puppet Agent Resources Skipped
 - Puppet Agent Resources Total

## Installation

Download the latest mkp (zipped) from the releases page.
Install the unzipped mkp either via the GUI or via the CLI.

See [MPK install](https://docs.checkmk.com/latest/en/mkps.html) for more information

## Contributing
Contributions are welcome! If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the GNU General Public License v2. See the LICENSE file for details.

## Acknowledgments
Based on work by
 Writen by Allan GooD: allan.cassaro@gmail.com
 https://github.com/allangood/check_mk/tree/master/plugins/puppet

(c) 2021 DECOIT GmbH
written by Timo Klecker: klecker@decoit.de

It contains the [checkmk](https://checkmk.com/) Enterprise Edition feature for baking agents and wato GUIs for parameter definition.