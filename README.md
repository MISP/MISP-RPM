# MISP-RPM

This RPMs work with a clean Red Hat installation. There are no external repositories like EPEL, Remi PHP or others needed. They only rely on optional official RHEL repositories and software collections - you'll obviously need a valid RedHat subscription attached.

If you want to use a full fletched MISP version with all available features like misp-modules, see [https://github.com/amuehlem/MISP-RPM/](https://github.com/amuehlem/MISP-RPM/). For this installation you'll need additional external repositories like EPEL and Remi PHP.

## Install

See [INSTALL.md](INSTALL.md) for this specific RPM install on RedHat and refer
to upstream MISP documentation for anything MISP related and/or upgrade paths.

## Reporting issues

Please report issues on this branch to https://github.com/MISP/MISP-RPM and not
to the original developers.

## RHEL8
The RHEL8 version can be found in the [rehl8](https://github.com/MISP/MISP-RPM/tree/rhel8) branch. Please switch to this branch if you want to see the corresponding files for RHEL8.

## Upgrading MISP
See the [upgrading instructions](UPGRADE.md) to upgrade MISP from our repository

## Simple Background jobs
See the [official documentation](https://www.circl.lu/doc/misp/appendices/#appendix-g-simplebackgroundjobs-migration-guide) how to activate the SimpleBackgroundJobs. Most important settings are
* ```/etc/supervisord.conf```
```
[inet_http_server]
port=127.0.0.1:9001
username=supervisor
password=securePasswordHere
```

* ```/etc/supervisord.d/misp-workers.ini```
see the [official documentation](https://www.circl.lu/doc/misp/appendices/#appendix-g-simplebackgroundjobs-migration-guide) for this file

* start and enable supervisord
```
systemctl enable supervisord
systemctl start supervisord
```

* enable SimpleBackgroundJobs in MISP
```
'SimpleBackgroundJobs' => array(
  'enabled' => true,
  'redis_host' => 'localhost',
  'redis_port' => 6379,
  'redis_password' => '',
  'redis_database' => 13,
  'redis_namespace' => 'background_jobs',
  'max_job_history_ttl' => 86400,
  'supervisor_host' => 'localhost',
  'supervisor_port' => 9001,
  'supervisor_user' => 'supervisor',
  'supervisor_password' => 'securePasswordHere',
),
```

* check the workers are started, status should be 'RUNNING' for all workers
```
supervisorctl -h http://localhost:9001 -u supervisor -p securePasswordHere status
```

## History
### Sep 20 2024
- release 2.4.198-1 for RHEL7
- release 2.4.198-1-el8, first version for RHEL8 systems

### Jul 11 2024
- release 2.4.194-1

### Apr 23 2024
- release 2.4.191-1

### Apr 2 2024
- release 2.4.188-1

### Feb 23 2024
- release 2.4.185-1

#### Feb 9 2024
- release 2.4.183-1
- release 2.4.184-1

#### Dec 19 2023
- release 2.4.182-1

#### Dec 12 2023
- release 2.4.181-1

#### Dec 8 2023
- Taking over the task to create this RPMS
- unforked the repository from https://github.com/amuehlem/MISP-RPM/
- lots of cleanup and adaption to the automated build environment
