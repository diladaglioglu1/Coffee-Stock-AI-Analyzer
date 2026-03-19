import React from "react";

/**
 * UI Designer Task: Dynamic Summary Cards
 * Colors mapped to specific Database Entities for visual hierarchy.
 */
const SummaryCard = ({ icon, title, value, subtitle, accent = "text-[#D98E5E]" }) => {
  return (
    <div className="bg-white border border-[#E9DED4] rounded-[2.5rem] p-8 shadow-sm hover:shadow-md transition-all duration-300 group">
      <div className={`flex items-center gap-3 mb-4 ${accent} transition-transform group-hover:scale-110`}>
        {icon}
        <span className="text-[10px] font-black uppercase tracking-[0.25em]">{title}</span>
      </div>
      <p className="text-4xl font-black text-[#1F1311] tracking-tighter">{value}</p>
      <p className="text-[11px] text-[#AFA19E] font-medium mt-2 uppercase tracking-wide">{subtitle}</p>
    </div>
  );
};

export default SummaryCard;