import React from "react";
import { ChevronRight, Coffee, Milk, Droplets, Leaf, Package } from "lucide-react";

const ProductListItem = ({ product, selected, onClick }) => {
  const getVisual = (name) => {
    const lower = name.toLowerCase();

    if (lower.includes("espresso") || lower.includes("beans")) {
      return { icon: Coffee, boxClass: "bg-[#2A1D1A] text-[#E6B89C]" };
    }

    if (lower.includes("milk")) {
      return { icon: Milk, boxClass: "bg-[#8DA3B8] text-[#F8FBFF]" };
    }

    if (lower.includes("syrup")) {
      return { icon: Droplets, boxClass: "bg-[#8B4513] text-[#FFF0E5]" };
    }

    if (lower.includes("matcha")) {
      return {
        icon: Leaf,
        boxClass: "bg-[#4E7A51] text-[#F3FFF2]",
      };
    }

    return { icon: Package, boxClass: "bg-[#F2EDE8] text-[#847B78]" };
  };

  const visual = getVisual(product.name);
  const Icon = visual.icon;

  return (
    <button
      onClick={onClick}
      className={`w-full rounded-[2rem] border p-5 text-left transition-all duration-300 ${
        selected
          ? "border-[#D98E5E] bg-[#FAF7F2] shadow-md scale-[1.02]"
          : "border-transparent hover:bg-[#F5F0EB]"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div
            className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 border shadow-inner ${visual.boxClass}`}
          >
            <Icon size={24} />
          </div>

          <div>
            <span
              className={`block text-[11px] font-black uppercase tracking-wide ${
                selected ? "text-[#1F1311]" : "text-[#847B78]"
              }`}
            >
              {product.name}
            </span>

            <div className="flex gap-2 mt-1 items-center">
              <span className="text-[10px] font-bold text-[#D98E5E]">
                {product.current_stock} {product.unit} available
              </span>
              <span className="text-[10px] text-[#AFA19E]">|</span>
              <span className="text-[10px] text-[#AFA19E]">
                ₺{product.unit_cost}
              </span>
            </div>
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