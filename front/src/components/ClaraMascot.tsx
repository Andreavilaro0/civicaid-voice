import { useEffect, useState, useRef, useCallback } from "react";
import { useLocation } from "react-router-dom";
import { useMascotState } from "@/hooks/useMascotState";

const SCENE_URL =
  "https://prod.spline.design/GkUXdIfFXTwByQ30/scene.splinecode";

// Spline canvas renders at native resolution, then CSS-scale + overflow-crop.
const RENDER_W = 1920;
const RENDER_H = 1080;

/** Responsive widget size based on viewport width and route */
function useWidgetSize(isChat: boolean, isHome: boolean) {
  const getSize = useCallback((w: number) => {
    if (isChat) return w < 640 ? 100 : w < 1024 ? 120 : 130;
    if (isHome) return w < 640 ? 120 : w < 1024 ? 160 : 200;
    return w < 640 ? 120 : w < 1024 ? 160 : 200;
  }, [isChat, isHome]);

  const [size, setSize] = useState(() => getSize(window.innerWidth));

  useEffect(() => {
    setSize(getSize(window.innerWidth));
    const onResize = () => setSize(getSize(window.innerWidth));
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [getSize]);

  return size;
}

/**
 * Adaptive scale + offset so the character fills the widget at any size.
 * Larger widgets → lower scale (see more scene). Smaller → zoom in.
 */
function getScaleAndOffset(widgetSize: number, smallRobot = false) {
  // Scale proportional to widget: 200px → 0.4, 120px → 0.5, 100px → 0.55
  let scale = Math.max(0.35, Math.min(0.6, 0.25 + (200 - widgetSize) * 0.0015));
  if (smallRobot) scale *= 0.55;
  const scaledW = RENDER_W * scale;
  const scaledH = RENDER_H * scale;
  const ox = -scaledW / 2 + widgetSize / 2;
  const oy = -scaledH / 2 + widgetSize / 2 + 10;
  return { scale, ox, oy };
}

/** CSS animation class per mascot state */
const stateAnimations: Record<string, string> = {
  idle: "animate-[float_3s_ease-in-out_infinite]",
  greeting: "animate-[bounce_0.6s_ease-in-out_3]",
  thinking: "animate-[pulse_1.2s_ease-in-out_infinite]",
  talking: "animate-[wiggle_0.3s_ease-in-out_infinite]",
};

export default function ClaraMascot() {
  const location = useLocation();
  const isChat = location.pathname === "/chat";
  const isHome = location.pathname === "/";
  const widgetSize = useWidgetSize(isChat, isHome);
  const { state } = useMascotState();
  const [routeBounce, setRouteBounce] = useState(false);
  const prevPath = useRef(location.pathname);
  const isMobile = widgetSize <= 100;

  // Bounce on route change
  useEffect(() => {
    if (location.pathname !== prevPath.current) {
      prevPath.current = location.pathname;
      setRouteBounce(true);
      const timer = setTimeout(() => setRouteBounce(false), 600);
      return () => clearTimeout(timer);
    }
  }, [location.pathname]);

  // Hide on mobile chat — would block the input area
  if (isChat && isMobile) return null;

  const animation = routeBounce
    ? "animate-[bounce_0.6s_ease-in-out]"
    : stateAnimations[state] ?? stateAnimations.idle;

  const smallRobot = isHome && widgetSize <= 120;
  const { scale, ox, oy } = getScaleAndOffset(widgetSize, smallRobot);

  return (
    <div
      className={`transition-all duration-500 ${animation}`}
      style={{
        width: widgetSize,
        height: widgetSize,
        overflow: "hidden",
        maxWidth: "100%",
        borderRadius: "1.25rem",
        opacity: isChat ? 0.85 : 1,
      }}
    >
      <div
        style={{
          width: RENDER_W,
          height: RENDER_H,
          transform: `scale(${scale})`,
          transformOrigin: "top left",
          marginLeft: ox,
          marginTop: oy,
          pointerEvents: "none",
        }}
      >
        <spline-viewer
          url={SCENE_URL}
          background="rgba(0,0,0,0)"
          loading="eager"
          events-target="none"
          style={{ width: RENDER_W, height: RENDER_H, display: "block", pointerEvents: "none" }}
        />
      </div>
    </div>
  );
}
