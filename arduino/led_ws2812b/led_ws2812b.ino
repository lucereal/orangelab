 #include <FastLED.h>                                                                                  
                  
  #define LED_PIN     4                                                                                 
  #define NUM_LEDS    38
  #define BRIGHTNESS  64

  CRGB leds[NUM_LEDS];

  void setup() {
    FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(BRIGHTNESS);
  }

  // Wipe a color across the strip
  void colorWipe(CRGB color, int delayMs) {
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = color;
      FastLED.show();
      delay(delayMs);
    }
  }

  // Fade all LEDs in and out
  void breathe(CRGB color, int steps, int delayMs) {
    for (int b = 0; b < 255; b += steps) {
      fill_solid(leds, NUM_LEDS, color);
      FastLED.setBrightness(b);
      FastLED.show();
      delay(delayMs);
    }
    for (int b = 255; b > 0; b -= steps) {
      fill_solid(leds, NUM_LEDS, color);
      FastLED.setBrightness(b);
      FastLED.show();
      delay(delayMs);
    }
  }

  // Rainbow that shifts over time
  void rainbow(int cycles, int delayMs) {
    for (int j = 0; j < 256 * cycles; j++) {
      for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CHSV((i * 256 / NUM_LEDS + j) & 255, 255, 255);
      }
      FastLED.show();
      delay(delayMs);
    }
  }

  // Sparkle random LEDs
  void sparkle(CRGB color, int count, int delayMs) {
    for (int i = 0; i < count; i++) {
      int pos = random(NUM_LEDS);
      leds[pos] = color;
      FastLED.show();
      delay(delayMs);
      leds[pos] = CRGB::Black;
    }
  }

  // Chase effect — single dot moving across strip
  void chase(CRGB color, int delayMs) {
    for (int i = 0; i < NUM_LEDS; i++) {
      fill_solid(leds, NUM_LEDS, CRGB::Black);
      leds[i] = color;
      // Dim trail
      if (i > 0) leds[i - 1] = color.nscale8(80);
      if (i > 1) leds[i - 2] = color.nscale8(20);
      FastLED.show();
      delay(delayMs);
    }
  }
  void flashFade(CRGB color, int delayMs) {
    fill_solid(leds, NUM_LEDS, color);
    FastLED.setBrightness(BRIGHTNESS);
    FastLED.show();
    delay(delayMs);
    for (int b = BRIGHTNESS; b >= 0; b--) {
      FastLED.setBrightness(b);
      FastLED.show();
      delay(50);
    }
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.setBrightness(BRIGHTNESS);
    FastLED.show();
  }

  void setColor(CRGB color, int delayMs, int b){
      fill_solid(leds, NUM_LEDS, color);
      FastLED.setBrightness(b);
      FastLED.show();
      delay(delayMs);
  }

  void loop() {
    // Reset brightness in case breathe changed it
    FastLED.setBrightness(BRIGHTNESS);
    int br = 100;
    // int b = 0;
    // int effectDelay = 200;
    // int pauseDelay = 300;
    // colorWipe(CRGB::Red, effectDelay);
    // colorWipe(CRGB::Black, effectDelay);

    // setColor(CRGB::Black, pauseDelay, b);

    // breathe(CRGB::Blue, 10, effectDelay);
    // setColor(CRGB::Black, pauseDelay, b);
   
    // // rainbow(3, effectDelay);
    // // setColor(CRGB::Black, pauseDelay, b);
    
    // flashFade(CRGB::Green, effectDelay);
    // setColor(CRGB::Black, pauseDelay, b);
    setColor(CRGB::Green, 5000, BRIGHTNESS);
    setColor(CRGB::Blue, 5000, BRIGHTNESS);
    setColor(CRGB::Red, 5000, BRIGHTNESS);

    setColor(CRGB::Green, 5000, br);
    setColor(CRGB::Blue, 5000, br);
    setColor(CRGB::Red, 5000, br);

    setColor(CRGB::Green, 5000, br + 100);
    setColor(CRGB::Blue, 5000, br + 100);
    setColor(CRGB::Red, 5000, br + 100);

    // setColor(CRGB::Green, 5000, 255);
    // setColor(CRGB::Blue, 5000, 255);
    // setColor(CRGB::Red, 5000, 255);
    
    // sparkle(CRGB::White, 50, effectDelay);
    // setColor(CRGB::Black, 500, b);

    // chase(CRGB::Green, effectDelay);
    // chase(CRGB::Purple, effectDelay);
    // setColor(CRGB::Black, 500, b);
  }
