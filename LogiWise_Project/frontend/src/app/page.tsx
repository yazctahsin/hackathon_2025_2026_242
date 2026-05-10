"use client";

import React, { useEffect, useState } from 'react';
import { getAiSummary, getOrders, runGhostSupport, notifyCustomer } from '@/lib/api';

import {
  LayoutDashboard,
  Package,
  AlertTriangle,
  MessageSquare,
  RefreshCw,
  TrendingUp,
  Truck,
  ShieldCheck,
  Clock3,
  Activity,
  Mail,
  ChevronRight
} from 'lucide-react';

// --- TYPES ---
interface Order {
  customer_name: string;
  current_step: number;
  status: string;
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  total_amount: number;
}

interface GhostAction {
  reason: string;
  actions: string[];
  priority: string;
  time: string;
  riskScore: number;
  factors: string[];
  customerName?: string;
}

// --- YARDIMCI BİLEŞEN: RISK SCORE DETAILS ---
const RiskScoreDetail = ({ score, factors }: { score: number, factors: string[] }) => (
  <div className="mt-4 p-4 bg-slate-900/50 rounded-xl border border-slate-700/50">
    <div className="flex justify-between items-center mb-3">
      <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider text-[10px]">AI Risk Analizi</span>
      <span className={`text-sm font-bold ${score > 70 ? 'text-red-400' : 'text-emerald-400'}`}>{score}/100</span>
    </div>
    <div className="w-full bg-slate-800 h-1.5 rounded-full mb-4 overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-1000 ${score > 70 ? 'bg-red-500' : 'bg-emerald-500'}`}
        style={{ width: `${score}%` }}
      />
    </div>
    <div className="grid grid-cols-2 gap-2">
      {factors.map((f, i) => (
        <div key={i} className="flex items-center gap-1.5 text-[9px] text-slate-500">
          <div className="w-1 h-1 rounded-full bg-blue-500/50" /> {f}
        </div>
      ))}
    </div>
  </div>
);

// --- YARDIMCI BİLEŞEN: ORDER TIMELINE ---
const OrderTimeline = ({ currentStep }: { currentStep: number }) => {
  const steps = ["Alındı", "Hazırlık", "Kargoda", "Teslim"];
  return (
    <div className="flex flex-col w-full max-w-[200px] mt-4">
      <div className="flex justify-between w-full mb-1">
        {steps.map((step, index) => (
          <span key={step} className={`text-[9px] font-medium ${index <= currentStep ? 'text-blue-400' : 'text-slate-600'}`} style={{ width: '20px', textAlign: 'center' }}>
            {step}
          </span>
        ))}
      </div>
      <div className="flex items-center px-1">
        {steps.map((step, index) => (
          <React.Fragment key={step}>
            <div className={`w-2.5 h-2.5 rounded-full border ${index <= currentStep ? 'bg-blue-500 border-blue-400 shadow-[0_0_8px_rgba(59,130,246,0.6)]' : 'bg-slate-800 border-slate-700'}`} />
            {index < steps.length - 1 && <div className={`h-[2px] flex-1 ${index < currentStep ? 'bg-blue-500' : 'bg-slate-700'}`} />}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default function Dashboard() {
  const [summary, setSummary] = useState<string>("Özet yükleniyor...");
  const [orders, setOrders] = useState<Order[]>([]);
  const [ghostActions, setGhostActions] = useState<GhostAction[]>([]);
  const [loading, setLoading] = useState(true);
  const [isMounted, setIsMounted] = useState(false);

  const handleNotify = async (customerName: string) => {
    try {
      await notifyCustomer(customerName, "Siparişiniz hakkında AI destekli bir güncelleme var.", "email");
      alert(`${customerName} başarıyla bilgilendirildi ✔`);
    } catch (err) {
      console.error(err);
      alert("Bildirim gönderilemedi.");
    }
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const [summaryData, ordersData] = await Promise.all([getAiSummary(), getOrders()]);
      if (summaryData) setSummary(summaryData.summary);
      if (ordersData) setOrders(ordersData);
    } catch (error) {
      console.error("Veri çekme hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGhostSupport = async () => {
    try {
      const data = await runGhostSupport();
      if (data.status === "success" && data.ai_action) {
        const newAction: GhostAction = {
          reason: data.ai_action.reason,
          actions: data.ai_action.actions || [],
          priority: data.ai_action.priority,
          time: "Az önce",
          riskScore: data.ml_risk_analysis?.score || 82,
          factors: data.ml_risk_analysis?.factors || [],
          customerName: data.target_customer_name || "Müşteri"
        };
        setGhostActions(prev => [newAction, ...prev]);
      }
    } catch (error) {
      console.error("Ghost Support Hatası:", error);
    }
  };

  useEffect(() => {
    setIsMounted(true);
    loadData();
  }, []);

  if (!isMounted) return <div className="min-h-screen bg-[#0f172a]" />;

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 p-6 font-sans">
      {/* HEADER */}
      <header className="flex justify-between items-center mb-8 bg-[#1e293b] p-4 rounded-xl border border-slate-700 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <LayoutDashboard size={24} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            LogiWise Dashboard <span className="text-xs font-normal text-slate-500 ml-2">v1.0 AI-Powered</span>
          </h1>
        </div>
        <button onClick={loadData} className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg transition-all border border-slate-600">
          <RefreshCw size={18} className={loading ? "animate-spin" : ""} /> Yenile
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-[#1e293b] border border-slate-700 rounded-2xl p-5 shadow-xl">
          <div className="flex justify-between items-center mb-2"><p className="text-slate-400 text-sm">Aktif Sevkiyat</p><Truck size={18} className="text-blue-400" /></div>
          <h2 className="text-3xl font-bold text-white">{orders.length}</h2>
        </div>
        <div className="bg-[#1e293b] border border-red-500/30 rounded-2xl p-5 shadow-xl">
          <div className="flex justify-between items-center mb-2"><p className="text-slate-400 text-sm">Riskli Sevkiyat</p><AlertTriangle size={18} className="text-red-400" /></div>
          <h2 className="text-3xl font-bold text-red-400">{ghostActions.length}</h2>
        </div>
        <div className="bg-[#1e293b] border border-green-500/30 rounded-2xl p-5 shadow-xl">
          <div className="flex justify-between items-center mb-2"><p className="text-slate-400 text-sm">Zamanında Teslim</p><ShieldCheck size={18} className="text-green-400" /></div>
          <h2 className="text-3xl font-bold text-green-400">%94</h2>
        </div>
        <div className="bg-[#1e293b] border border-blue-500/30 rounded-2xl p-5 shadow-xl">
          <div className="flex justify-between items-center mb-2"><p className="text-slate-400 text-sm">Bugünkü Teslimat</p><Clock3 size={18} className="text-blue-400" /></div>
          <h2 className="text-3xl font-bold text-blue-400">38</h2>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <section className="bg-gradient-to-br from-[#1e293b] to-[#0f172a] p-6 rounded-2xl border border-blue-500/30 shadow-2xl relative overflow-hidden">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 text-blue-400"><MessageSquare size={20} /> Günlük Operasyon Özeti (Gemini AI)</h2>
            <div className="text-slate-300 italic border-l-4 border-blue-500 pl-4 bg-blue-500/5 py-4 rounded-r-lg">"{summary}"</div>
          </section>

          <section className="bg-[#1e293b] rounded-2xl border border-slate-700 shadow-xl overflow-hidden">
            <div className="p-4 border-b border-slate-700 bg-slate-900/50 flex justify-between items-center">
              <h2 className="font-semibold flex items-center gap-2"><Package size={20} className="text-indigo-400" /> Aktif Sevkiyatlar</h2>
              <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-1 rounded-full">{orders.length} Kayıt</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="text-xs uppercase text-slate-500 bg-slate-900/50">
                  <tr><th className="p-4">Müşteri</th><th className="p-4">Durum / Risk</th><th className="p-4">Tutar</th></tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {orders.map((order, i) => (
                    <tr key={i} className="hover:bg-slate-800/50 transition-colors">
                      <td className="p-4"><div className="text-white font-medium">{order.customer_name}</div><OrderTimeline currentStep={order.current_step} /></td>
                      <td className="p-4 space-y-2">
                        <span className={`px-2 py-1 rounded text-[10px] font-bold block w-fit ${order.status === 'Hazırlanıyor' ? 'bg-amber-500/20 text-amber-500' : 'bg-emerald-500/20 text-emerald-500'}`}>{order.status}</span>
                        <div className={`px-2 py-0.5 rounded-full text-[9px] font-bold border animate-pulse w-fit ${order.risk_level === "HIGH" ? "bg-red-500/20 text-red-400 border-red-500/30" : "bg-green-500/20 text-green-400 border-green-500/30"}`}>{order.risk_level} RISK</div>
                      </td>
                      <td className="p-4 text-slate-400 font-mono text-sm">₺{order.total_amount?.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <div className="space-y-6">
          <section className="bg-slate-900 p-6 rounded-2xl border border-rose-500/30 shadow-xl min-h-[500px]">
            <div className="flex flex-col items-center mb-6">
              <div className="bg-rose-500/20 p-4 rounded-full mb-3"><AlertTriangle size={32} className="text-rose-500" /></div>
              <h2 className="text-xl font-bold text-white">Ghost Support AI</h2>
              <p className="text-slate-500 text-sm text-center">Anomali tespiti ve proaktif çözüm</p>
            </div>
            <button onClick={handleGhostSupport} className="w-full bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg flex items-center justify-center gap-2 mb-6">
              <Activity size={18} /> Operasyonu Denetle
            </button>
            <div className="space-y-4">
              {ghostActions.length === 0 && <div className="text-center text-slate-600 text-sm mt-10">Henüz riskli bir durum algılanmadı.</div>}
              {ghostActions.map((action, i) => (
                <div key={i} className="bg-slate-800 p-4 rounded-xl border-l-4 border-rose-500 animate-in slide-in-from-right duration-300">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-rose-400 font-bold text-[10px] uppercase tracking-widest">Kritik Uyarı</span>
                    <span className="text-[10px] text-slate-500">{action.time}</span>
                  </div>
                  <p className="text-sm text-slate-200 mb-1 leading-tight font-medium">{action.reason}</p>
                  <RiskScoreDetail score={action.riskScore} factors={action.factors} />
                  <div className="bg-slate-950 p-3 rounded-lg border border-slate-700/50 my-4">
                    <p className="text-[10px] text-slate-500 mb-2 font-bold flex items-center gap-1"><ChevronRight size={12} className="text-rose-500" /> AI Aksiyon Planı:</p>
                    <ul className="space-y-1.5">
                      {action.actions?.map((a: string, idx: number) => (
                        <li key={idx} className="text-xs text-rose-300 flex gap-2"><span className="text-rose-500">•</span> {a}</li>
                      ))}
                    </ul>
                  </div>
                  <button
                    onClick={() => handleNotify(action.customerName || "Müşteri")}
                    className="w-full flex items-center justify-center gap-2 py-2 bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 border border-blue-500/30 rounded-lg transition-all text-xs font-semibold"
                  >
                    <Mail size={14} /> Bilgilendirme Gönder
                  </button>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}