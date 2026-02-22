import "react";

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      "spline-viewer": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          url?: string;
          background?: string;
          "events-target"?: string;
          loading?: "eager" | "lazy";
        },
        HTMLElement
      >;
    }
  }
}
