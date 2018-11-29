#define DEBUG

#ifdef DEBUG
  #include <SoftwareSerial.h>
#endif

#define PIN_ENABLE_LEFT 10 
#define PIN_ENABLE_RIGHT 11

#define PIN_LEFT_FORWARD 9
#define PIN_LEFT_BACKWARD 8

#define PIN_RIGHT_FORWARD 6
#define PIN_RIGHT_BACKWARD 7

#define BOARD_LED 13

#define UART_BAUDRATE 9600

#include "l298n.h"

#ifdef DEBUG
  #define SERIAL_UART mySerial
  #define M_SERIAL Serial
  SoftwareSerial SERIAL_UART(3, 2); // RX, TX
#else
   #define SERIAL_UART Serial
#endif


/* method pfefix */
static const uint8_t SLAVE_ID = 0x60;
static const uint8_t MASTER_ID = 0xD0;

/* response methods */
static const uint8_t METHOD_SPEED = 0x01 ^ SLAVE_ID;
static const uint8_t METHOD_STATE = 0x02 ^ SLAVE_ID;

static const uint8_t METHOD_FIXED_SPEED = 0x06 ^ SLAVE_ID;
static const uint8_t METHOD_REPEAT_LAST = 0x08 ^ SLAVE_ID;

/* request methods */
static const uint8_t CMD_SET_SPEED = 0x01;
static const uint8_t CMD_GET_STATE = 0x02;
static const uint8_t CMD_STOP      = 0x03;

static const uint8_t CMD_FIX_LEFT  = 0x06;
static const uint8_t CMD_FIX_RIGHT = 0x07;

static const uint8_t CMD_REPEAT_LAST = 0x08;

static speed_t speed = {0, 0};
static state_t state;


// static uint8_t response[8];

void setup() {
  pinMode(PIN_ENABLE_LEFT, OUTPUT);
  pinMode(PIN_ENABLE_RIGHT, OUTPUT);

  pinMode(PIN_LEFT_FORWARD, OUTPUT);
  pinMode(PIN_LEFT_BACKWARD, OUTPUT);
  pinMode(PIN_RIGHT_FORWARD, OUTPUT);
  pinMode(PIN_RIGHT_BACKWARD, OUTPUT);

  pinMode(BOARD_LED, OUTPUT);

  digitalWrite(BOARD_LED, 1);

  SERIAL_UART.begin(UART_BAUDRATE);

  while (!SERIAL_UART) { /* Waiting for Serial */ }
  
#ifdef DEBUG
    M_SERIAL.begin(UART_BAUDRATE);
#endif

  digitalWrite(BOARD_LED, 0);
}

void loop() {
  uint8_t command = 0;


  if( SERIAL_UART.available() ) {
    command = SERIAL_UART.read() ^ MASTER_ID;
    
    switch( command )
    {
    case CMD_SET_SPEED:
      digitalWrite(BOARD_LED, 1);
      while( ! SERIAL_UART.available() ) {}
      speed.left = SERIAL_UART.read();
      while( ! SERIAL_UART.available() ) {}
      speed.right = SERIAL_UART.read();      

      generate_signals(speed, state);
      emit(state);

#ifdef DEBUG
        M_SERIAL.print("Updated: ");
        M_SERIAL.print(state.left); 
        M_SERIAL.print(" ");
        M_SERIAL.println(state.right); 
        M_SERIAL.print("\t");
        M_SERIAL.print(state.left_forward); 
        M_SERIAL.print(" "); 
        M_SERIAL.print(state.left_backward); 
        M_SERIAL.print("    "); 
        M_SERIAL.print(state.right_forward); 
        M_SERIAL.print(" "); 
        M_SERIAL.println(state.right_backward); 
#endif

      digitalWrite(BOARD_LED, 0);
      break;

    case CMD_GET_STATE:
      SERIAL_UART.write(METHOD_STATE);
      SERIAL_UART.write(state.left);
      SERIAL_UART.write(state.right);
      SERIAL_UART.write(state.left_forward);
      SERIAL_UART.write(state.left_backward);
      SERIAL_UART.write(state.right_forward);
      SERIAL_UART.write(state.right_backward);
      break;
    
    case CMD_STOP:
      speed.left = 0;
      speed.right = 0;

      generate_signals(speed, state);
      emit(state);
      
#ifdef DEBUG
        M_SERIAL.print("stop");
#endif
      break;
  
    default:
    
#ifdef DEBUG
        M_SERIAL.print("wtf: ");
        M_SERIAL.println(command); 
#endif

      digitalWrite(BOARD_LED, 1);
      delay(500);
      digitalWrite(BOARD_LED, 0);
      delay(250);
      digitalWrite(BOARD_LED, 1);
      delay(500);
      digitalWrite(BOARD_LED, 0);
      break;
    }
    
    SERIAL_UART.flush();
  }
}




//void emit_response(const uint8_t* response, uint8_t byte_count) {
//  for( uint8_t i = 0; i < byte_count; ++i ) {
//    Serial.write(response[i]);
//    Serial.flush();
//  }
//}
