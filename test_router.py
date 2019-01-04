import unittest

from router import Router

class TestRouter(unittest.TestCase):

  def test_wan_hostname(self):
    router = Router()
    router.wan_hostname="hostname"
    self.assertTrue(router.wan_hostname == "hostname")
    self.assertTrue(router.nvram['wan_hostname'] == "hostname")

  def test_router_name(self):
    router = Router()
    router.router_name="hostname"
    self.assertTrue(router.router_name == "hostname")
    self.assertTrue(router.nvram['router_name'] == "hostname")

  def test_name(self):
    router = Router()
    router.name="hostname"
    self.assertTrue(router.name == "hostname")
    self.assertTrue(router.router_name == "hostname")
    self.assertTrue(router.nvram['router_name'] == "hostname")
    self.assertTrue(router.wan_hostname == "hostname")
    self.assertTrue(router.nvram['wan_hostname'] == "hostname")

  def test_passwd(self):
    from passlib.hash import md5_crypt
    router = Router()
    router.password = "HellYeah!"
    self.assertTrue(md5_crypt.verify("HellYeah!", router.nvram['http_passwd']))

  def test_leases(self):
    from ddwrtnvram import readNvram, writeNvram
    from nvramlogging import getTestLogger
    logger = getTestLogger()
    nvram = readNvram ('./test/static.lease.23.bin', logger)
    router = Router(nvram)
    leases = router.leases
    self.assertEqual(len(leases), 2)
    self.assertEqual(leases[0].hostname, "raspberrypi")
    self.assertEqual(leases[1].hostname, "raspberrypi2")
    from lease import Lease
    printerLease = Lease({"hostname": "printer",
      "mac_address": "aa:bb:f8:43:f6:dd",
      "ip_address": "192.168.235.88",
      "lease_time": "500"})
    router.addLease(printerLease)
    leases = router.leases
    self.assertEqual(len(leases), 3)
    self.assertEqual(router.nvram['static_leasenum'], '3')
    self.assertEqual(leases[0].hostname, "printer")
    self.assertEqual(leases[1].hostname, "raspberrypi")
    self.assertEqual(leases[2].hostname, "raspberrypi2")
    self.assertEqual(router.leasesStr(), "AA:BB:F8:43:F6:DD=printer=192.168.235.88=500 B8:27:EB:5E:9C:C0=raspberrypi=192.168.23.41=3600 B8:27:EB:5E:9C:C1=raspberrypi2=192.168.23.42=3601 ")

    # now write, read and then retest
    writeNvram('./test/test.static.leases.router.bin', router.nvram, logger)
    nvram = readNvram ('./test/test.static.leases.router.bin', logger)
    router = Router(nvram)
    leases = router.leases
    self.assertEqual(len(leases), 3)
    self.assertEqual(router.nvram['static_leasenum'], '3')
    self.assertEqual(leases[1].hostname, "raspberrypi")
    self.assertEqual(leases[2].hostname, "raspberrypi2")
    self.assertEqual(leases[0].hostname, "printer")


  def test_change_sshd_status(self):
    nvram = {}
    router = Router(nvram)
    router.changeSshdStatus(True)
    self.assertEqual(router.nvram['sshd_enable'], '1')
    self.assertEqual(router.nvram['sshd_port'], '22')
    self.assertEqual(router.nvram['sshd_passwd_auth'], '0')
    self.assertEqual(router.nvram['sshd_authorized_keys'], '')
    self.assertEqual(router.nvram['sshd_forwarding'], '0')

    router.changeSshdStatus(False)
    self.assertEqual(router.nvram['sshd_enable'], '0')

  def test_enable_wan_ssh(self):
    nvram = {}
    router = Router(nvram)
    router.changeSshdStatus(True)
    router.enableWanSsh(enableRemoteAccess=True, wanPort=66)
    self.assertEqual(router.nvram['remote_mgt_ssh'], '1')
    self.assertEqual(router.nvram['sshd_wanport'], '66')

    router.enableWanSsh(enableRemoteAccess=False)
    self.assertEqual(router.nvram['remote_mgt_ssh'], '0')

  def test_enable_ssh_key_auth(self):
    nvram = {}
    router = Router(nvram)
    router.changeSshdStatus(True)


    authorized_keys = ['ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGgXglKfhxM27daib6JRgfBv1iCxMedRzGFOANN0HuebUWXzwgf+KtwWMK2/rQzxuZIDC6a2cNXMkU/pRiTrHwBP/L+PNfF6Xq+U/3pKjou776U1uNKT4pBdi6aBhAb30mkK81CAArh+lp5/ZpwRsMAnSJ4H6j9j7aUhkL70iKMe3glBjnL+HmETOxC/X3u28llMkEHt4ipOhRLD9+669HILyUfEYKbFvIKI9ZPGnV1ZbP1Ci/5DvThHHuF1lWB691r63kZdy3CKGvtqyT5e2sCpLhwIAWE/DOXx9tunZugTOiegLCyEizf9rNe8eMIvRVkMoXptxi5Bn1Oq2UGLqH vinod@Thinkpad',
                       'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmNQmpuQSQR5iphz+hVZve+no3+TtfLoN8J2MjALtZ1RgiHyIV/q0KnClGz0n+55/bHO3UzDzq+Ps5SnMJcosk8Ywp0Rt0GfTOAAp5qrCvfnb1AihPDoFcOXK/uqrRV5IeY3he3VZ33kCjQ6nFMRFVnSFiTU9JSL05Wi0wmQTD1t/EbLr2m2FhalGh7YzBArJKFJbUEpTFuPHZrdcuQiD9hKxyz6HiZOiplOHGtbVAqrow62zLNHOpquI0NXwuKbD9DaeMmGnbibYurYNEVtnGDKTGTVUn3Pc8EjkjKuZyJpsdB/jZcpvSjcoJGSm17+K6QVriBJy4acUfQWOWaUAd vinod@vinod']

    router.enableSshKeyAuth(authorized_keys)

    shouldBe = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGgXglKfhxM27daib6JRgfBv1iCxMedRzGFOANN0HuebUWXzwgf+KtwWMK2/rQzxuZIDC6a2cNXMkU/pRiTrHwBP/L+PNfF6Xq+U/3pKjou776U1uNKT4pBdi6aBhAb30mkK81CAArh+lp5/ZpwRsMAnSJ4H6j9j7aUhkL70iKMe3glBjnL+HmETOxC/X3u28llMkEHt4ipOhRLD9+669HILyUfEYKbFvIKI9ZPGnV1ZbP1Ci/5DvThHHuF1lWB691r63kZdy3CKGvtqyT5e2sCpLhwIAWE/DOXx9tunZugTOiegLCyEizf9rNe8eMIvRVkMoXptxi5Bn1Oq2UGLqH vinod@Thinkpad\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmNQmpuQSQR5iphz+hVZve+no3+TtfLoN8J2MjALtZ1RgiHyIV/q0KnClGz0n+55/bHO3UzDzq+Ps5SnMJcosk8Ywp0Rt0GfTOAAp5qrCvfnb1AihPDoFcOXK/uqrRV5IeY3he3VZ33kCjQ6nFMRFVnSFiTU9JSL05Wi0wmQTD1t/EbLr2m2FhalGh7YzBArJKFJbUEpTFuPHZrdcuQiD9hKxyz6HiZOiplOHGtbVAqrow62zLNHOpquI0NXwuKbD9DaeMmGnbibYurYNEVtnGDKTGTVUn3Pc8EjkjKuZyJpsdB/jZcpvSjcoJGSm17+K6QVriBJy4acUfQWOWaUAd vinod@vinod\n'
    self.assertEqual(router.nvram['sshd_authorized_keys'], shouldBe)
