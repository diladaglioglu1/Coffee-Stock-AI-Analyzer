import React from "react";
import { Coffee, Milk, Droplets, Leaf, Package } from "lucide-react";

/** * Person 5 Task: Dynamic Product Card with Stock Alerts
 */
const ProductCard = ({ name, current_stock, unit, unit_cost, highlight }) => {
  const isLowStock = current_stock < 15; // Robustness logic for visual warnings

  const getVisual = (productName) => {
    const lower = productName.toLowerCase();
    if (lower.includes("beans")) return { icon: Coffee, iconClass: "text-[#E6B89C]", boxClass: "bg-[#2A1D1A] border-[#3A2722]" };
    if (lower.includes("milk")) return { icon: Milk, iconClass: "text-[#F8FBFF]", boxClass: "bg-[#8DA3B8] border-[#9FB3C6]" };
    if (lower.includes("syrup")) return { icon: Droplets, iconClass: "text-[#FFF0E5]", boxClass: "bg-[#8B4513] border-[#9C592C]" };
    if (lower.includes("matcha")) return { icon: Leaf, iconClass: "text-[#F3FFF2]", boxClass: "bg-[#4E7A51] border-[#638F66]" };
    return { icon: Package, iconClass: "text-[#847B78]", boxClass: "bg-[#F2EDE8] border-[#E7DED5]" };
  };

  const visual = getVisual(name);
  const Icon = visual.icon;

  return (
    <div className={`p-8 rounded-[2.5rem] border shadow-sm transition-all duration-500 hover:shadow-2xl ${highlight ? "bg-gradient-to-br from-[#2D1F1B] to-[#3A2722] text-white" : "bg-white border-[#F2EDE8]"}`}>
      <div className="flex justify-between items-start mb-10">
        <div className={`w-14 h-14 rounded-2xl flex items-center justify-center border shadow-inner ${visual.boxClass}`}><Icon size={24} className={visual.iconClass} /></div>
        {isLowStock && (
          <span className="text-[9px] font-black px-3 py-1 rounded-full bg-red-500 text-white animate-pulse uppercase tracking-widest">LOW STOCK</span>
        )}
      </div>
      <h3 className={`text-[10px] font-black uppercase tracking-widest mb-3 ${highlight ? "text-[#AFA19E]" : "text-[#847B78]"}`}>{name}</h3>
      <div className="flex items-baseline gap-2 mb-4 font-black tracking-tighter">
        <span className="text-5xl">{current_stock}</span><span className="text-[10px] uppercase opacity-60 tracking-normal">{unit}</span>
      </div>
      <div className="pt-4 border-t border-white/10 flex justify-between items-center text-[11px] opacity-80 font-bold">
        <span>Unit Cost</span><span>₺{unit_cost}</span>
      </div>
    </div>
  );
};

export default ProductCard;