import React from "react";
import {
  Coffee,
  Milk,
  Droplets,
  Leaf,
  GlassWater,
  Bean,
  Package,
} from "lucide-react";

const ProductCard = ({ name, current_stock, unit, unit_cost, highlight }) => {
  const getVisual = (productName) => {
    const lower = productName.toLowerCase();

    if (
      lower.includes("espresso") ||
      lower.includes("beans") ||
      lower.includes("coffee")
    ) {
      return {
        icon: Coffee,
        iconClass: "text-[#E6B89C]",
        boxClass: "bg-[#2A1D1A] border-[#3A2722]",
        dark: true,
      };
    }

    if (lower.includes("whole milk")) {
      return {
        icon: Milk,
        iconClass: "text-[#F8FBFF]",
        boxClass: "bg-[#8DA3B8] border-[#9FB3C6]",
      };
    }

    if (lower.includes("oat milk")) {
      return {
        icon: GlassWater,
        iconClass: "text-[#FFF5EA]",
        boxClass: "bg-[#C89B6D] border-[#D8AE83]",
      };
    }

    if (lower.includes("almond milk")) {
      return {
        icon: GlassWater,
        iconClass: "text-[#FFF5EA]",
        boxClass: "bg-[#B88A68] border-[#C69A79]",
      };
    }

    if (lower.includes("soy milk")) {
      return {
        icon: GlassWater,
        iconClass: "text-[#F3F7F0]",
        boxClass: "bg-[#7D9B76] border-[#91AE8A]",
      };
    }

    if (lower.includes("syrup")) {
      return {
        icon: Droplets,
        iconClass: "text-[#FFF0E5]",
        boxClass: "bg-[#8B4513] border-[#9C592C]",
      };
    }

    if (lower.includes("matcha")) {
      return {
        icon: Leaf,
        iconClass: "text-[#F3FFF2]",
        boxClass: "bg-[#4E7A51] border-[#638F66]",
      };
    }

    if (lower.includes("cocoa")) {
      return {
        icon: Bean,
        iconClass: "text-[#FFF1EA]",
        boxClass: "bg-[#7A4A3A] border-[#8B5B4B]",
      };
    }

    return {
      icon: Package,
      iconClass: "text-[#847B78]",
      boxClass: "bg-[#F2EDE8] border-[#E7DED5]",
      dark: false,
    };
  };

  const visual = getVisual(name);
  const Icon = visual.icon;
  const isDarkCard = visual.dark;

  return (
    <div
      className={`p-8 rounded-[2.5rem] border shadow-sm transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 ${
        isDarkCard
          ? "bg-gradient-to-br from-[#2D1F1B] to-[#3A2722]"
          : "bg-white border-[#F2EDE8]"
      }`}
    >
      <div className="flex justify-between items-start mb-10">
        <div
          className={`w-16 h-16 rounded-2xl flex items-center justify-center shadow-inner border ${visual.boxClass}`}
        >
          <Icon size={28} className={visual.iconClass} />
        </div>

        {highlight && (
          <div className="text-[10px] font-black px-3 py-1 rounded-full uppercase tracking-[0.18em] bg-[#D98E5E]/10 text-[#D98E5E] border border-[#D98E5E]/10">
            Featured
          </div>
        )}
      </div>

      <h3
        className={`text-xs font-black uppercase tracking-[0.2em] mb-3 ${
          isDarkCard ? "text-[#AFA19E]" : "text-[#847B78]"
        }`}
      >
        {name}
      </h3>

      <div className="flex items-baseline gap-2 mb-4">
        <span
          className={`text-5xl font-black tracking-tighter ${
            isDarkCard ? "text-white" : "text-[#1F1311]"
          }`}
        >
          {current_stock}
        </span>
        <span
          className={`text-[10px] font-bold uppercase tracking-widest ${
            isDarkCard ? "text-[#847B78]" : "text-[#AFA19E]"
          }`}
        >
          {unit}
        </span>
      </div>

      <div className="flex items-center justify-between text-[11px]">
        <span className={isDarkCard ? "text-[#AFA19E]" : "text-[#847B78]"}>
          Unit Cost
        </span>
        <span
          className={`font-bold ${
            isDarkCard ? "text-white" : "text-[#1F1311]"
          }`}
        >
          ₺{unit_cost}
        </span>
      </div>
    </div>
  );
};

export default ProductCard;