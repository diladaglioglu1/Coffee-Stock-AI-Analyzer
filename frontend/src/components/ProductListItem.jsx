import React from "react";
import {
  ChevronRight,
  Coffee,
  Milk,
  Droplets,
  Leaf,
  GlassWater,
  Bean,
  Package,
} from "lucide-react";

const ProductListItem = ({ product, selected, onClick }) => {
  const getVisual = (name) => {
    const lower = name.toLowerCase();

    if (
      lower.includes("espresso") ||
      lower.includes("beans") ||
      lower.includes("coffee")
    ) {
      return {
        icon: Coffee,
        iconClass: "text-[#E6B89C]",
        boxClass: "bg-[#2A1D1A] border-[#3A2722]",
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
    };
  };

  const visual = getVisual(product.name);
  const Icon = visual.icon;

  return (
    <button
      onClick={onClick}
      className={`w-full rounded-[2rem] border p-5 text-left transition-all ${
        selected
          ? "border-[#D98E5E] bg-[#FAF7F2] shadow-md"
          : "border-transparent hover:bg-[#F5F0EB]"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div
            className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 border ${visual.boxClass}`}
          >
            <Icon size={24} className={visual.iconClass} />
          </div>

          <div>
            <span
              className={`block text-[11px] font-black uppercase tracking-wide ${
                selected ? "text-[#1F1311]" : "text-[#847B78]"
              }`}
            >
              {product.name}
            </span>

            <span className="text-xs text-[#AFA19E]">
              {product.current_stock} {product.unit} available
            </span>
          </div>
        </div>

        <ChevronRight
          size={16}
          className={selected ? "text-[#D98E5E]" : "text-[#AFA19E]"}
        />
      </div>
    </button>
  );
};

export default ProductListItem;