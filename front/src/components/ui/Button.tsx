"use client";

import { Button as AriaButton } from "react-aria-components";
import type { ButtonProps as AriaButtonProps } from "react-aria-components";

type Variant = "primary" | "secondary" | "ghost";

interface ButtonProps extends Omit<AriaButtonProps, "children"> {
  variant?: Variant;
  icon?: React.ReactNode;
  fullWidth?: boolean;
  children?: React.ReactNode;
}

const variantStyles: Record<Variant, string> = {
  primary:
    "bg-clara-blue text-white data-[hovered]:bg-[#164d66] data-[pressed]:bg-[#123f54]",
  secondary:
    "bg-white text-clara-text border-2 border-clara-border data-[hovered]:border-clara-blue data-[pressed]:bg-clara-card",
  ghost:
    "bg-transparent text-clara-blue data-[hovered]:bg-clara-info data-[pressed]:bg-clara-card",
};

export default function Button({
  variant = "primary",
  icon,
  fullWidth = false,
  children,
  className = "",
  ...props
}: ButtonProps) {
  return (
    <AriaButton
      className={`
        inline-flex items-center justify-center gap-3
        min-h-touch min-w-touch px-6
        rounded-xl font-body text-button font-medium
        transition-colors duration-150
        data-[focus-visible]:outline data-[focus-visible]:outline-[3px]
        data-[focus-visible]:outline-clara-blue data-[focus-visible]:outline-offset-2
        data-[disabled]:opacity-50 data-[disabled]:cursor-not-allowed
        ${variantStyles[variant]}
        ${fullWidth ? "w-full" : ""}
        ${className}
      `}
      {...props}
    >
      {icon && <span aria-hidden="true">{icon}</span>}
      {children}
    </AriaButton>
  );
}
