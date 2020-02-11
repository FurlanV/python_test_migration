from ..classes.Credentials import Credentials
from ..classes.MountPoint import MountPoint
from ..classes.Workload import Workload
from ..classes.Migration import Source, Migration, MigrationTarget
from ..classes.Persistence import Persistence

import unittest
import time
import os


class TestCredentials(unittest.TestCase):
    def test_username_not_str(self):
        self.assertRaises(ValueError, Credentials, 123, 'password', 'domain')

    def test_password_not_str(self):
        self.assertRaises(
            ValueError, Credentials, 'username', [], 'domain')

    def test_domain_not_str(self):
        self.assertRaises(
            ValueError, Credentials, 'username', 'password', True)

    def test_proper_credintials(self):
        c = Credentials('Vinicius', 'ViniciusPassword', 'my_domain')
        self.assertEqual(c.username, 'Vinicius')
        self.assertEqual(c.password, 'ViniciusPassword')
        self.assertEqual(c.domain, 'my_domain')


class TestMountPoint(unittest.TestCase):
    def test_name_not_str(self):
        self.assertRaises(ValueError, MountPoint, 1, 50)

    def test_size_not_int(self):
        self.assertRaises(ValueError, MountPoint, 'c:', '100')

    def test_proper_mount_point(self):
        mp = MountPoint('c:', 100)
        self.assertEqual(mp.name, 'c:')
        self.assertEqual(mp.size, 100)


class TestSource(unittest.TestCase):
    def setUp(self):
        self.s = Source('192.168.1.1', 'user', 'pass')
        self.s_specific_source = Source('192.168.1.1', 'user', 'pass')

    def test_ip_none(self):
        self.assertRaises(ValueError, Source, None, 'user', 'pass')

    def test_username_none(self):
        self.assertRaises(ValueError, Source, '192.168.1.1', None, 'pass')

    def test_password_none(self):
        self.assertRaises(ValueError, Source, '192.168.1.1', 'user', None)

    def test_change_username(self):
        username = self.s.get_username()
        self.s.change_username("user2")
        self.assertEqual(self.s.get_username(), "user2")
        self.s.change_username(username)

    def test_change_username_to_none(self):
        self.assertRaises(ValueError, self.s.change_username, None)

    def test_change_password(self):
        password = self.s.get_password()
        self.s.change_password("pass2")
        self.assertEqual(self.s.get_password(), "pass2")
        self.s.change_password(password)

    def test_change_password_to_none(self):
        self.assertRaises(ValueError, self.s.change_password, None)

    def test_proper_source(self):
        self.assertEqual(self.s.get_ip(), '192.168.1.1')
        self.assertEqual(self.s.get_username(), 'user')
        self.assertEqual(self.s.get_password(), 'pass')


class TestWorkload(unittest.TestCase):
    def setUp(self):
        self.credentials = Credentials('vinicius', 'viniciusPassword', 'my_domain')
        self.storage = [MountPoint('c:', 100), MountPoint('d:', 100)]

    def test_ip_not_str(self):
        self.assertRaises(ValueError, Workload, 123,self.credentials, self.storage)

    def test_storage_not_list(self):
        self.assertRaises(ValueError, Workload, '192.168.1.1', self.credentials, MountPoint('c:', 100))

    def test_storage_not_list_of_mountpoint_class(self):
        self.assertRaises(ValueError, Workload, '192.168.1.1', self.credentials, [1, 2, 3])

    def test_proper_workload(self):
        wl = Workload('192.168.1.1', self.credentials, self.storage)
        self.assertEqual(wl.ip, '192.168.1.1')
        self.assertEqual(wl.credentials, self.credentials)
        self.assertEqual(wl.storage, self.storage)


class TestMigrationTarget(unittest.TestCase):
    
    def setUp(self):
        self.cloud_credentials = Credentials('vinicius', 'viniciusPassword', 'my_domain')
        self.credentials = Credentials('vinicius', 'viniciusPassword', 'my_domain')
        self.storage = [MountPoint('c:', 100), MountPoint('d:', 100)]
        self.target_vm = Workload('192.168.1.1', self.credentials, self.storage)
        self.mt = MigrationTarget(self.cloud_credentials, "aws", self.target_vm)

    def test_cloud_type_not_str(self):
        self.assertRaises(ValueError, MigrationTarget, 123, self.cloud_credentials, self.target_vm)

    def test_cloud_type_not_in_set(self):
        self.assertRaises(ValueError, MigrationTarget, "amazon", self.cloud_credentials, self.target_vm)

    def test_cloud_credintials_not_credentials_class(self):
        self.assertRaises(ValueError, MigrationTarget, "aws", 'user:pass', self.target_vm)

    def test_target_vm_not_workload_class(self):
        self.assertRaises(ValueError, MigrationTarget, "aws", self.cloud_credentials, "target")

    def test_proper_migrationtarget(self):
        self.assertEqual(self.mt.get_cloud_type(), "aws")
        self.assertEqual(self.mt.credentials, self.cloud_credentials)
        self.assertEqual(self.mt.vm_target, self.target_vm)


class TestMigration(unittest.TestCase):
    
    def setUp(self):
        self.selected_mountPoints = [MountPoint('c:', 100)]

        self.selected_absent_mount_points = [MountPoint('c:', 100), MountPoint('z:', 100)]

        self.source_credentials = Credentials('Vinicius', 'ViniciusPassword', 'my_domain')

        self.source_storage = [MountPoint('c:', 100), MountPoint('d:', 100), MountPoint('e:', 100)]

        self.source = Workload('192.168.1.1', self.source_credentials, self.source_storage)

        self.cloud_credentials = Credentials('ViniciusCloud', 'ViniciuCloudsPassword', 'my_domain')

        self.target_credentials = Credentials('Vinicius', 'ViniciusPassword', 'my_domain')

        self.target_storage = [MountPoint('f:', 100), MountPoint('g:', 100)]

        self.target_vm = Workload('192.168.1.1', self.target_credentials, self.target_storage)

        self.target = MigrationTarget(self.cloud_credentials, "aws", self.target_vm)

        self.migration = Migration(self.selected_mountPoints, self.source, self.target)

    def test_selected_mountPoints_not_list(self):
        self.assertRaises(ValueError, Migration, "asd", self.source,self.target)

    def test_selected_mountPoints_not_list_of_mountpoint(self):
        self.assertRaises(ValueError, Migration, [1, 2, 3], self.source, self.target)

    def test_source_not_workload_class(self):
        self.assertRaises(ValueError, Migration, self.selected_mountPoints, "source", self.target)

    def test_target_not_migrationtarget_class(self):
        self.assertRaises(ValueError, Migration, self.selected_mountPoints, self.source, "target")

    def test_proper_migration(self):
        self.assertEqual(self.migration.selected_mountPoints, self.selected_mountPoints)
        self.assertEqual(self.migration.source, self.source)
        self.assertEqual(self.migration.target, self.target)

    def test_run_error_migration_volume_c_is_not_allowed(self):
        self.migration.IS_C_ALLOWED = False
        self.migration.run()
        self.assertEqual(self.migration.state, "error")

    def test_run_error_migration_selected_storages_are_absent(self):
        self.migration_abs = Migration(self.selected_absent_mount_points, self.source, self.target)
        self.migration_abs.run()
        self.assertEqual(self.migration_abs.state, "error")

    def test_run_successful(self):
        self.migration.run()
        self.assertEqual(self.migration.state, "success")
        self.assertEqual(self.target_vm.ip, self.source.ip)
        self.assertEqual(self.target_vm.credentials, self.source.credentials)
        selected_mountpoints_are_in_target_storage =\
            False not in [x.name in [y.name for y in self.target_vm.storage]
                          for x in self.selected_mountPoints]
        copied_target_storage_elements_are_equal_to_source_ones =\
            False not in [x in self.source.storage
                          for x in self.target_vm.storage
                          if x.name in
                          [y.name for y in self.selected_mountPoints]]
        self.assertTrue(selected_mountpoints_are_in_target_storage)
        self.assertTrue(
            copied_target_storage_elements_are_equal_to_source_ones)
        self.assertEqual([(x.name, x.size) for x in self.target_vm.storage],
                         [("f:", 100), ("g:", 100), ("c:", 100)])


class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.source_source = Source('192.168.1.1', 'user', 'pass')

        self.source_source_with_different_ip = Source('192.168.1.2','user','pass')

        self.selected_mountPoints = [MountPoint('c:', 100)]

        self.source_credentials = Credentials('Vinicius',
                                              'ViniciusPassword',
                                              'my_domain')

        self.source_storage = [MountPoint('c:', 100), MountPoint('d:', 100), MountPoint('e:', 100)]

        self.source = Workload('192.168.1.1', self.source_credentials, self.source_storage)

        self.source_with_different_ip = Workload('192.168.1.2', self.source_credentials, self.source_storage)

        self.cloud_credentials = Credentials('ViniciusCloud',
                                             'ViniciusCloudPass',
                                             'my_cloud')

        self.target_credentials = Credentials('Vinicius',
                                              'ViniciusPassword',
                                              'my_domain')

        self.target_storage = [MountPoint('f:', 100), MountPoint('g:', 100)]

        self.target_vm = Workload('192.168.2.1', self.target_credentials, self.target_storage)

        self.target = MigrationTarget(self.cloud_credentials, "aws", self.target_vm)

        self.migration = Migration(self.selected_mountPoints, self.source, self.target)

        self.migration_with_different_ip = Migration(self.selected_mountPoints, self.source_with_different_ip, self.target)

        self.obj_list = [self.selected_mountPoints,
                          self.source_credentials,
                          self.source_storage,
                          self.source,
                          self.cloud_credentials,
                          self.target_credentials,
                          self.target_storage,
                          self.target_vm,
                          self.target,
                          self.migration]

    def test_delete(self):
        
        if os.path.exists('dump.pickle'):
            os.remove('dump.pickle')
        
        self.assertFalse(os.path.exists('dump.pickle'))
        
        with open('dump.pickle', 'w'):
            pass
        
        self.assertTrue(os.path.exists('dump.pickle'))
        pl = Persistence([], 'dump.pickle')
        pl.delete()
        
        self.assertFalse(os.path.exists('dump.pickle'))

    def test_create_read(self):
        
        if os.path.exists('dump.pickle'):
            os.remove('dump.pickle')
        
        self.assertFalse(os.path.exists('dump.pickle'))
        
        pl1 = Persistence(self.obj_list, 'dump.pickle')
        pl1.create(self.obj_list)
        self.assertTrue(os.path.exists('dump.pickle'))
        
        self.assertEqual(self.obj_list, self.obj_list)

if __name__ == "__main__":
    unittest.main()
