import { useEffect, useState } from 'react';

export default function CustomCursor() {
  const [position, setPosition] = useState({ x: -1000, y: -1000 });

  useEffect(() => {
    let animationFrameId;

    const updatePosition = (e) => {
      // Use requestAnimationFrame to smoothen out high-refresh-rate mouse movements
      cancelAnimationFrame(animationFrameId);
      animationFrameId = requestAnimationFrame(() => {
        setPosition({ x: e.clientX, y: e.clientY });
      });
    };
    
    window.addEventListener('mousemove', updatePosition);
    return () => {
      window.removeEventListener('mousemove', updatePosition);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div
      className="fixed pointer-events-none z-[-1]"
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        width: '800px',
        height: '800px',
        transform: 'translate(-50%, -50%)',
        // A soft, atmospheric blue/white lighting effect
        background: 'radial-gradient(circle, rgba(226, 232, 240, 0.12) 0%, rgba(226, 232, 240, 0) 50%)',
        filter: 'blur(60px)',
        // Instantly follows the mouse but feels natural due to the massive blurry radius
        transition: 'transform 0.1s linear', 
      }}
    />
  );
}
