const int BTN_1 = 17;
const int BTN_2 = 6;
const int LAMP_TALK = 2;
const int POT = A0;
const int H_SLIDER = A1;
const int V_SLIDER = A2;

struct Button {
  char pin, name;
  bool pressed;
};

Button btn_1 = { 17, '1', false };
Button btn_2 = { 6, '2', false };
Button btn_3 = { 8, '3', false };
Button btn_4 = { 10, '4', false };
Button btn_5 = { 12, '5', false };
Button btn_6 = { 13, '6', false };
Button btn_red = { 4, 'r', false };
Button btn_green = { 3, 'g', false };
Button btn_black = { 14, 'k', false };
Button clr_white = { 15, 'W', false };
Button clr_black = { 7, 'K', false };
Button clr_blue = { 11, 'B', false };
Button clr_green = { 9, 'G', false };
Button clr_red = { 16, 'R', false };
Button clr_yellow = { 5, 'Y', false };
Button btn_talk = { 18, 'T', false };
Button enc_1a = { 44, '{', false };
Button enc_1b = { 42, '}', false };

Button* all_buttons[] = { &btn_1, &btn_2, &btn_3, &btn_4, &btn_5, &btn_6, &btn_black, &btn_green, &btn_red, &clr_red, &clr_green, &clr_blue, &clr_yellow, &clr_black, &clr_white, &btn_talk, &enc_1a, &enc_1b };

int nButtons = 18;
int timeBtnTalk = 0;
bool sleep = true;

void setup() {

  for (int i = 0; i < nButtons; i++) {
    pinMode((*all_buttons[i]).pin, INPUT_PULLUP);
  }
  Serial.begin(115200);

  pinMode(LAMP_TALK, OUTPUT);
}

void loop() {
  for (int i = 0; i < nButtons; i++) {
    (*all_buttons[i]).pressed = !digitalRead((*all_buttons[i]).pin);
    Serial.print((*all_buttons[i]).pressed ? (*all_buttons[i]).name : '.');
  }

  Serial.print(" ");
  Serial.print(analogRead(POT));
  Serial.print(" ");
  Serial.print(analogRead(H_SLIDER));
  Serial.print(" ");
  Serial.print(analogRead(V_SLIDER));
  Serial.println();

  float a = (sin(millis() / 300.) + 1) / 2 * 200 + 55;

  if (btn_talk.pressed) {
    timeBtnTalk = millis();
  }

  sleep = millis() - timeBtnTalk > 2000;

  int brightness = btn_talk.pressed ? 255 : sleep ? a : 0;

  analogWrite(LAMP_TALK, brightness);

  delay(10);
}
