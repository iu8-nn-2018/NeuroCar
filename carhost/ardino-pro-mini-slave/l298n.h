
struct speed_t
{
    int8_t left;
    int8_t right;
};

struct state_t
{
    uint8_t left;
    uint8_t right;
  
    uint8_t left_forward;
    uint8_t left_backward;
    uint8_t right_forward;
    uint8_t right_backward;
};

int generate_signals(const speed_t& speed, state_t& state)
{  
    if ( speed.left == 0 ) {
        state.left = 0;
        state.left_forward = 0;
        state.left_backward = 0;
  
    } else if ( speed.left > 0 ) {
        state.left = speed.left << 1;
        state.left_forward = 1;
        state.left_backward = 0;
  
    } else { /* if (speed.left < 0) */
        state.left = (abs(speed.left) << 1);
        state.left_forward = 0;
        state.left_backward = 1;
    }
  
  
    if ( speed.right == 0 ) {
        state.right = 0;
        state.right_forward = 0;
        state.right_backward = 0;
  
    } else if ( speed.right > 0 ) {
        state.right = speed.right << 1;
        state.right_forward = 1;
        state.right_backward = 0;
  
    } else { /* if (speed.right < 0) */
        state.right = (abs(speed.right) << 1);
        state.right_forward = 0;
        state.right_backward = 1;
    }
  
    return 0;
}


int emit(const state_t& state)
{
    analogWrite(PIN_ENABLE_LEFT, state.left);
    analogWrite(PIN_ENABLE_RIGHT, state.right);
  
    digitalWrite(PIN_LEFT_FORWARD, state.left_forward);
    digitalWrite(PIN_LEFT_BACKWARD, state.left_backward);
    digitalWrite(PIN_RIGHT_FORWARD, state.right_forward);
    digitalWrite(PIN_RIGHT_BACKWARD, state.right_backward);

    return 0;
}
