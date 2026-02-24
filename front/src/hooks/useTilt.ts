import { useRef, useState, useCallback } from "react";

/**
 * useTilt — 3D tilt effect on hover, extracted from PersonasSection TiltCard.
 * Returns ref, tilt state, hovering flag, and event handlers.
 */
export function useTilt(maxDeg = 12) {
  const ref = useRef<HTMLDivElement>(null);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [hovering, setHovering] = useState(false);

  const onMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      const card = ref.current;
      if (!card) return;
      const rect = card.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const rotateX = ((e.clientY - centerY) / (rect.height / 2)) * -maxDeg;
      const rotateY = ((e.clientX - centerX) / (rect.width / 2)) * maxDeg;
      setTilt({ x: rotateX, y: rotateY });
    },
    [maxDeg]
  );

  const onMouseEnter = useCallback(() => setHovering(true), []);

  const onMouseLeave = useCallback(() => {
    setTilt({ x: 0, y: 0 });
    setHovering(false);
  }, []);

  const style: React.CSSProperties = {
    transform: `rotateX(${tilt.x}deg) rotateY(${tilt.y}deg) scale(${hovering ? 1.02 : 1})`,
    transition: hovering ? "transform 0.1s ease-out" : "transform 0.4s ease-out",
    transformStyle: "preserve-3d",
  };

  const handlers = { onMouseMove, onMouseEnter, onMouseLeave };

  return { ref, tilt, hovering, style, handlers };
}
