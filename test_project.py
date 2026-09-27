import pytest
from project import set_ball_1_spawn_state, set_ball_2_spawn_state, draw_ui_frame

def main():
    test_set_ball_1_spawn_state()
    test_set_ball_2_spawn_state()
    test_draw_ui_frame()

def test_set_ball_1_spawn_state():
    assert set_ball_1_spawn_state() == True

def test_set_ball_2_spawn_state():
    assert set_ball_2_spawn_state() == True

def test_draw_ui_frame():
    with pytest.raises(ValueError):
        draw_ui_frame(x = 'string', y = 5, width = 10, height = 10)
    with pytest.raises(ValueError):
        draw_ui_frame(x = 1, y ='1', width = 10, height = 10)
    with pytest.raises(ValueError):
        draw_ui_frame(x = 1, y = 5, width = '10', height = 10)
    with pytest.raises(ValueError):
        draw_ui_frame(x = 1, y = 5, width = 10, height = '10')

if __name__ == "__main__":
    main()