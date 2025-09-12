// Logos and icon assets manifest for easy imports across the app.
// Import whatever exists; Vite will convert these to optimized URLs at build time.

// Primary wordmarks
import LogoSvg from './logo.svg';
// Optional alternates
import LogoCroppedPng from './logo-cropped.png';

// Icon set (if present in this folder)
import Icon16 from './icon-16x16.png';
import Icon32 from './icon-32x32.png';
import Icon48 from './icon-48x48.png';
import Icon72 from './icon-72x72.png';
import Icon96 from './icon-96x96.png';
import Icon128 from './icon-128x128.png';
import Icon192 from './icon-192x192.png';
import Icon256 from './icon-256x256.png';
import Icon512 from './icon-512x512.png';
import AppleTouch180 from './apple-touch-icon-180x180.png';

export const logos = {
  primary: LogoSvg,
  cropped: LogoCroppedPng,
};

export const icons = {
  '16': Icon16,
  '32': Icon32,
  '48': Icon48,
  '72': Icon72,
  '96': Icon96,
  '128': Icon128,
  '192': Icon192,
  '256': Icon256,
  '512': Icon512,
  appleTouch180: AppleTouch180,
};

// Sensible defaults
export const defaultLogo = LogoSvg;
export const defaultIcon = Icon192;

export default {
  logos,
  icons,
  defaultLogo,
  defaultIcon,
};

