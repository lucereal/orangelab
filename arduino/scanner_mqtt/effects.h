#pragma once
#include <FastLED.h>

extern CRGB leds[];

void colorWipe(CRGB color, int delayMs) {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = color;
    FastLED.show();
    delay(delayMs);
  }
}

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
  FastLED.setBrightness(BRIGHTNESS);
}

void rainbow(int cycles, int delayMs) {
  for (int j = 0; j < 256 * cycles; j++) {
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CHSV((i * 256 / NUM_LEDS + j) & 255, 255, 255);
    }
    FastLED.show();
    delay(delayMs);
  }
}

void sparkle(CRGB color, int count, int delayMs) {
  for (int i = 0; i < count; i++) {
    int pos = random(NUM_LEDS);
    leds[pos] = color;
    FastLED.show();
    delay(delayMs);
    leds[pos] = CRGB::Black;
  }
  FastLED.show();
}

void flashFade(CRGB color, int delayMs) {
  fill_solid(leds, NUM_LEDS, color);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.show();
  delay(delayMs);
  for (int b = BRIGHTNESS; b >= 0; b--) {
    FastLED.setBrightness(b);
    FastLED.show();
    delay(10);
  }
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.show();
}

void chase(CRGB color, int delayMs) {

  for (int i = 0; i < NUM_LEDS; i++) {
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    leds[i] = color;
    if (i > 0) leds[i - 1] = color.nscale8(80);
    if (i > 1) leds[i - 2] = color.nscale8(20);
    FastLED.show();
    delay(delayMs);
  }
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
}
