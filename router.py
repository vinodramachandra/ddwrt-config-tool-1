class Router:

  def __init__(self, nvram={}):
    self.nvram = nvram

  @property
  def wan_hostname(self):
    return self.nvram['wan_hostname']

  @wan_hostname.setter
  def wan_hostname(self, value):
    self.nvram['wan_hostname'] = value

  @property
  def router_name(self):
    return self.nvram['router_name']

  @router_name.setter
  def router_name(self, value):
    self.nvram['router_name'] = value

  @property
  def name(self):
    return self.nvram['router_name']

  @name.setter
  def name(self, value):
    self.router_name = value
    self.wan_hostname = value
