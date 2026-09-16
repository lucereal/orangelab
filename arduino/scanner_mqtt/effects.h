#pragma once
#include <FastLED.h>

extern CRGB leds[];

struct FlashFadeState {
  bool active = false;
  bool holding = false;
  CRGB color = CRGB::Black;
  int brightness = 0;
  unsigned long holdUntil = 0;
  unsigned long lastStep = 0;
  int holdMs = 250;
  int stepMs = 10;
};

FlashFadeState flashFadeState;

void startFlashFade(CRGB color, int holdMs) {
  flashFadeState.active = true;
  flashFadeState.holding = true;
  flashFadeState.color = color;
  flashFadeState.brightness = BRIGHTNESS;
  flashFadeState.holdMs = holdMs;
  flashFadeState.holdUntil = millis() + holdMs;
  flashFadeState.lastStep = millis();
  fill_solid(leds, NUM_LEDS, color);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.show();
}

void updateFlashFade() {
  if (!flashFadeState.active) {
    return;
  }

  unsigned long now = millis();
  if (flashFadeState.holding) {
    if ((long)(now - flashFadeState.holdUntil) < 0) {
      return;
    }
    flashFadeState.holding = false;
    flashFadeState.lastStep = now;
    return;
  }

  if ((long)(now - flashFadeState.lastStep) < flashFadeState.stepMs) {
    return;
  }
  flashFadeState.lastStep = now;
  flashFadeState.brightness--;

  if (flashFadeState.brightness <= 0) {
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.setBrightness(BRIGHTNESS);
    FastLED.show();
    flashFadeState.active = false;
    return;
  }

  FastLED.setBrightness(flashFadeState.brightness);
  FastLED.show();
}
