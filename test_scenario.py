from test_api import *


@pytest.mark.asyncio
@pytest.mark.scenario
async def test_scenario():
    assert await test_create_menu(), "1. test_create_menu error"
    assert await test_create_submenu(), "2. test_create_submenu error"
    assert await test_create_dish(), "3. test_create_dish error"
    assert await test_create_dish(), "4. test_create_dish error"
    assert await test_get_menu(), "5. test_get_menu error"
    assert await test_get_submenu(), "6. test_get_submenu error"
    assert await test_delete_submenu(), "7. test_delete_submenu error"
    assert await test_get_submenus(), "8. test_get_submenus error"
    assert await test_get_dishes(), "9. test_get_dishes error"
    assert await test_get_menu(), "10. test_get_menu error"
    assert await test_delete_menu(), "11. test_delete_menu error"
    assert await test_get_menus(), "12. test_get_menus error"
    