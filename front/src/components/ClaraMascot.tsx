import { useEffect, useState, useRef, useCallback } from "react";
import { useLocation } from "react-router-dom";
import { useMascotState } from "@/hooks/useMascotState";

const SCENE_URL =
  "https://prod.spline.design/GkUXdIfFXTwByQ30/scene.splinecode";

// Render at native resolution, CSS-scale + overflow-crop to widget size.
const RENDER_W = 1920;
const RENDER_H = 1080;
const SCALE = 0.4;
const OFFSET_X = -(RENDER_W * SCALE) / 2;
const OFFSET_Y = -(RENDER_H * SCALE) / 2 + 20;

/** Responsive widget size based on viewport width and route */
function useWidgetSize(isChat: boolean) {
  const getSize = useCallback((w: number) => {
    if (isChat) return w < 1024 ? 100 : 130;
    return w < 640 ? 120 : w < 1024 ? 160 : 200;
  }, [isChat]);

  const [size, setSize] = useState(() => getSize(window.innerWidth));

  useEffect(() => {
    setSize(getSize(window.innerWidth));
    const onResize = () => setSize(getSize(window.innerWidth));
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [getSize]);

  return size;
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
  const widgetSize = useWidgetSize(isChat);
  const { state } = useMascotState();
  const [routeBounce, setRouteBounce] = useState(false);
  const prevPath = useRef(location.pathname);
  const isMobile = widgetSize <= 120;

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

  // Center offsets depend on widget size
  const ox = OFFSET_X + widgetSize / 2;
  const oy = OFFSET_Y + widgetSize / 2;

  return (
    <div
      className={`transition-all duration-500 ${animation}`}
      style={{
        width: widgetSize,
        height: widgetSize,
        overflow: "hidden",
        borderRadius: "1.25rem",
        opacity: isChat ? 0.8 : 1,
      }}
    >
      <div
        style={{
          width: RENDER_W,
          height: RENDER_H,
          transform: `scale(${SCALE})`,
          transformOrigin: "top left",
          marginLeft: ox,
          marginTop: oy,
        }}
      >
        <spline-viewer
          url={SCENE_URL}
          background="rgba(0,0,0,0)"
          loading="eager"
          style={{ width: RENDER_W, height: RENDER_H, display: "block" }}
        />
      </div>
    </div>
  );
}
