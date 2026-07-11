from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field
from playwright.async_api import (
    Browser,
    async_playwright,
)

from ichika_generator import create_ichika_html


browser: Browser | None = None
playwright_instance = None


class IchikaRequest(BaseModel):
    raceDate: str
    place: str
    raceNo: str

    honmei: str
    stamp: str = "なし"

    nigeRate: int = Field(
        ge=0,
        le=100,
    )

    upRate: int = Field(
        ge=-30,
        le=30,
    )

    selectedBoats: list[str]

    boatScores: dict[str, int]
    boatComments: dict[str, str]

    mainComment: str = ""

    wave: int = Field(
        ge=0,
        le=100,
    )

    dangerBoat: str = "なし"
    motorEval: str = ""

    characterImage: str = ""
    backgroundImage: str = ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    global browser
    global playwright_instance

    playwright_instance = (
        await async_playwright().start()
    )

    browser = await playwright_instance.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    )

    yield

    if browser:
        await browser.close()

    if playwright_instance:
        await playwright_instance.stop()


app = FastAPI(
    title="BOAT STRIKE Image API",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://boat-strike.online",
        "https://www.boat-strike.online",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }


@app.post(
    "/generate/ichika/zenjitsu",
    response_class=Response,
)
async def generate_ichika_zenjitsu(
    payload: IchikaRequest,
):
    if browser is None:
        raise HTTPException(
            status_code=503,
            detail="Browser is not ready",
        )

    page = await browser.new_page(
        viewport={
            "width": 1100,
            "height": 1800,
        },
        device_scale_factor=2,
    )

    try:
        html_text = create_ichika_html(
            payload.model_dump()
        )

        await page.set_content(
            html_text,
            wait_until="networkidle",
        )

        await page.evaluate(
            """
            async () => {
              if (document.fonts?.ready) {
                await document.fonts.ready;
              }

              const images = [
                ...document.images
              ];

              await Promise.all(
                images.map((image) => {
                  if (image.complete) {
                    return Promise.resolve();
                  }

                  return new Promise((resolve) => {
                    image.addEventListener(
                      "load",
                      resolve,
                      { once: true }
                    );

                    image.addEventListener(
                      "error",
                      resolve,
                      { once: true }
                    );
                  });
                })
              );
            }
            """
        )

        target = page.locator("#newspaper")

        await target.wait_for(
            state="visible",
        )

        png_bytes = await target.screenshot(
            type="png",
            animations="disabled",
            scale="device",
        )

        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition":
                    'inline; filename="ichika-zenjitsu.png"',
                "Cache-Control":
                    "no-store",
            },
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

    finally:
        await page.close()
