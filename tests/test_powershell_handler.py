from app.services.powershell_handler import get_system_apps

def test_get_list_of_system_apps():
    apps = get_system_apps()
    assert isinstance(apps, list), "Expected a list of applications"
    assert len(apps) > 0, "Expected at least one application in the list"
    for app in apps:
        assert isinstance(app, dict), "Each application should be a dictionary"
        assert 'Type' in app, "Each application should have a 'Type' key"
        assert 'Name' in app, "Each application should have a 'Name' key"
        assert 'AppID' in app, "Each application should have an 'AppID' key"
        assert isinstance(app['Type'], str), "'Type' should be a string"
        assert isinstance(app['Name'], str), "'Name' should be a string"
        assert isinstance(app['AppID'], str), "'AppID' should be a string"