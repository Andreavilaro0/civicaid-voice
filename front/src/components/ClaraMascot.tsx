import { useEffect, useState, useRef } from "react";
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

/** Responsive widget size based on viewport width */
function useWidgetSize() {
  const [size, setSize] = useState(() =>
    window.innerWidth < 640 ? 120 : window.innerWidth < 1024 ? 160 : 200,
  );

  useEffect(() => {
    const onResize = () => {
      const w = window.innerWidth;
      setSize(w < 640 ? 120 : w < 1024 ? 160 : 200);
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

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
  const widgetSize = useWidgetSize();
  const { state } = useMascotState();
  const location = useLocation();
  const [routeBounce, setRouteBounce] = useState(false);
  const prevPath = useRef(location.pathname);
  const isChat = location.pathname === "/chat";
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
        // Slightly smaller & more transparent on chat page
        opacity: isChat ? 0.85 : 1,
        transform: isChat ? "scale(0.75)" : undefined,
        transformOrigin: "bottom right",
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
