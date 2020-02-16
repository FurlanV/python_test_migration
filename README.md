# python_test_migration

### How to execute tests to this code.

- Install python >= 3.5
- Clone or download this repository
- Extract the folder 'python_test_migration' in your computer
- To execute the tests, in your terminal run:

python -m python_test_migration.tests.test_classes


### Implement following set of classes in Python.

Class Workload that contains following fields:
- IP string, credentials of type Credentials
- Storage that contains list of instances of type MountPoint

Class Credentials that contains the following fields
- Username - string
- Password - string
- Domain - string

Class MountPoint that contains the following fields:
- Mount point name - string - Example: “c:\”
- Total size of the mount point - int

Add following business constraints to class Workload:
- Username, password, IP should not be None
- IP cannot change for the specific workload
- You cannot have more than one source with the same IP

Class MigrationTarget that contains following fields:
- Cloud Type: aws, azure, vsphere, vcloud - no other types are allowed
- Cloud Credentials of type Credentials
- Target Vm object of type Workload

Define class Migration that contains the following
- Selected Mount points: list of MountPoint
- Source of type WorkloadMigrationTarget of type MigrationTarget
- Migration state: not started, running, error, success

- Implement run() method - run method should sleep for X min (simulate running migration) copy source object to the MigrationTarget.TargetVM and target should only have mount points that are selected. For example, if source has: C:\ D: and E:\ and only C: was selected, target should only have C:\

- Implement business logic to not allow running migrations when volume C:\ is not allowed

- Implement persistence layer to allow to save all those classes into filesystem. It should allow to create, update, read and delete objects.
