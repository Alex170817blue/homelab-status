from homelab_status.main import get_status
def test_get_status():
   assert get_status() == "Homelab is alive!"
