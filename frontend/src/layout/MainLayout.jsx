import React from "react";
import { LayoutDashboard, Sparkles, Coffee, Bell } from "lucide-react";

const MainLayout = ({ children, activeTab, setActiveTab }) => {
  return (
    <div className="flex min-h-screen bg-[#FDFBF9] font-sans text-[#1F1311]">
      <aside className="w-24 bg-[#1A0F0E] flex flex-col items-center py-10 gap-12 sticky top-0 h-screen shadow-2xl z-20">
        <div className="w-14 h-14 bg-[#D98E5E] rounded-2xl flex items-center justify-center text-white shadow-lg">
          <Coffee size={32} strokeWidth={1.5} />
        </div>

        <nav className="flex flex-col gap-10">
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`flex flex-col items-center gap-2 transition-all ${
              activeTab === "dashboard"
                ? "text-[#D98E5E]"
                : "text-[#847B78] hover:text-white"
            }`}
          >
            <div
              className={`p-4 rounded-2xl ${
                activeTab === "dashboard" ? "bg-[#2A1D1A]" : ""
              }`}
            >
              <LayoutDashboard size={24} />
            </div>
            <span className="text-[10px] font-black uppercase tracking-tighter">
              DASHBOARD
            </span>
          </button>

          <button
            onClick={() => setActiveTab("analysis")}
            className={`flex flex-col items-center gap-2 transition-all ${
              activeTab === "analysis"
                ? "text-[#D98E5E]"
                : "text-[#847B78] hover:text-white"
            }`}
          >
            <div
              className={`p-4 rounded-2xl ${
                activeTab === "analysis" ? "bg-[#2A1D1A]" : ""
              }`}
            >
              <Sparkles  size={24} />
            </div>
            <span className="text-[10px] font-black uppercase tracking-tighter text-center">
              AI Analysis
            </span>
          </button>
        </nav>
      </aside>

      <div className="flex-1 flex flex-col relative">
        <header className="flex items-center justify-between px-16 py-10 bg-[#FDFBF9] border-b border-[#F2EDE8]">
          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.35em] text-[#AFA19E] mb-3">
              Coffee Inventory Dashboard
            </p>
            <h1 className="text-4xl md:text-5xl font-black tracking-[-0.05em] text-[#1F1311] leading-none uppercase">
              BrewIntelligence
            </h1>
            <div className="h-1.5 w-24 bg-[#D98E5E] mt-4 mb-3 rounded-full"></div>
            <p className="text-[#847B78] font-bold text-[10px] uppercase tracking-[0.45em] opacity-80">
              Inventory Intelligence & Forecasting
            </p>
          </div>

          <div className="flex items-center gap-5">
            <button className="w-12 h-12 rounded-2xl border border-[#E9DED4] bg-white flex items-center justify-center text-[#847B78] shadow-sm hover:shadow-md transition">
              <Bell size={20} />
            </button>

            <div className="w-14 h-14 bg-[#E5DCD4] rounded-full border-2 border-white shadow-md flex items-center justify-center text-2xl">
              ☕
            </div>
          </div>
        </header>

        <main className="p-10 md:p-12 lg:p-16 flex-1 bg-[#FDFBF9]">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;