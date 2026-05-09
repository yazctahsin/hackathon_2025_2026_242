"use client";
import React, { useEffect, useState } from 'react';
import { getAiSummary, getOrders, runGhostSupport } from '@/lib/api';
import { 
  LayoutDashboard, 
  Package, 
  AlertTriangle, 
  MessageSquare, 
  RefreshCw, 
  TrendingUp
} from 'lucide-react';

export default function Dashboard() {
  const [summary, setSummary] = useState<string>("Özet yükleniyor...");
  const [orders, setOrders] = useState<any[]>([]);
  const [ghostActions, setGhostActions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    try {
      const [summaryData, ordersData] = await Promise.all([
        getAiSummary(),
        getOrders()
      ]);
      setSummary(summaryData.summary);
      setOrders(ordersData);
    } catch (error) {
      console.error("Veri çekme hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGhostSupport = async () => {
    try {
      const data = await runGhostSupport();
      
      // Backend'den başarılı yanıt geldiyse ve risk tespit edildiyse
      if (data.status === "success" && data.ai_action) {
        const newAction = {
          // Backend'den gelen adet bilgisini ve Gemini'nin analizini birleştiriyoruz
          reason: `${data.risky_orders_count} Riskli Sipariş Analizi: ${data.ai_action.reason}`,
          // Gemini'nin önerdiği aksiyon mesajı
          action: data.ai_action.action,
          time: "Az önce"
        };
        setGhostActions(prev => [newAction, ...prev]);
      } else if (data.status === "Safe") {
        alert(data.message); // "Risk bulunamadı" uyarısı
      }
    } catch (error) {
      console.error("Ghost Support Hatası:", error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 p-6 font-sans">
      {/* Header */}
      <header className="flex justify-between items-center mb-8 bg-[#1e293b] p-4 rounded-xl border border-slate-700 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <LayoutDashboard size={24} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            LogiWise Dashboard <span className="text-xs font-normal text-slate-500 ml-2">v1.0 AI-Powered</span>
          </h1>
        </div>
        <button 
          onClick={loadData}
          className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg transition-all border border-slate-600"
        >
          <RefreshCw size={18} className={loading ? "animate-spin" : ""} /> Yenile
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Sol Kolon: Operasyon Özeti (Gemini) */}
        <div className="lg:col-span-2 space-y-6">
          <section className="bg-gradient-to-br from-[#1e293b] to-[#0f172a] p-6 rounded-2xl border border-blue-500/30 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <TrendingUp size={80} />
            </div>
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 text-blue-400">
              <MessageSquare size={20} /> Günlük Operasyon Özeti (Gemini AI)
            </h2>
            <div className="text-slate-300 leading-relaxed italic border-l-4 border-blue-500 pl-4 bg-blue-500/5 py-4 rounded-r-lg">
              "{summary}"
            </div>
          </section>

          {/* Sipariş Listesi */}
          <section className="bg-[#1e293b] rounded-2xl border border-slate-700 shadow-xl overflow-hidden">
            <div className="p-4 border-b border-slate-700 bg-slate-800/50 flex justify-between items-center">
              <h2 className="font-semibold flex items-center gap-2">
                <Package size={20} className="text-indigo-400" /> Aktif Sevkiyatlar
              </h2>
              <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-1 rounded-full">{orders.length} Kayıt</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead className="text-xs uppercase text-slate-500 bg-slate-900/50">
                  <tr>
                    <th className="p-4">Müşteri</th>
                    <th className="p-4">Ürün</th>
                    <th className="p-4">Adet</th>
                    <th className="p-4">Durum</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {orders.map((order, i) => (
                    <tr key={i} className="hover:bg-slate-800/50 transition-colors group">
                      <td className="p-4 font-medium text-white">{order.customer_name}</td>
                      <td className="p-4 text-slate-400">{order.product_name || "Belirtilmemiş"}</td>
                      <td className="p-4">{order.quantity || 1}</td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          order.status === 'Hazırlanıyor' ? 'bg-amber-500/20 text-amber-500' : 'bg-emerald-500/20 text-emerald-500'
                        }`}>
                          {order.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        {/* Sağ Kolon: Ghost Support */}
        <div className="space-y-6">
          <section className="bg-slate-900 p-6 rounded-2xl border border-rose-500/30 shadow-xl min-h-[500px]">
            <div className="flex flex-col items-center mb-6">
              <div className="bg-rose-500/20 p-4 rounded-full mb-3">
                <AlertTriangle size={32} className="text-rose-500" />
              </div>
              <h2 className="text-xl font-bold text-white">Ghost Support AI</h2>
              <p className="text-slate-500 text-sm text-center">Gecikme tespiti ve otomatik müşteri iletişimi</p>
            </div>

            <button 
              onClick={handleGhostSupport}
              className="w-full bg-rose-600 hover:bg-rose-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-rose-900/20 flex items-center justify-center gap-2 mb-6"
            >
              Riskleri Tara ve Aksiyon Al
            </button>

            <div className="space-y-4">
              {ghostActions.length === 0 && (
                <div className="text-center text-slate-600 text-sm mt-10">
                  Henüz bir risk analizi yapılmadı.
                </div>
              )}
              {ghostActions.map((action, i) => (
                <div key={i} className="bg-slate-800 p-4 rounded-xl border-l-4 border-rose-500 animate-in slide-in-from-right duration-300">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-rose-400 font-bold text-xs uppercase text-[10px]">Risk Tespit Edildi</span>
                    <span className="text-[10px] text-slate-500">{action.time}</span>
                  </div>
                  <p className="text-sm text-slate-200 mb-3 leading-tight">{action.reason}</p>
                  <div className="bg-slate-950 p-3 rounded-lg border border-slate-700/50">
                     <p className="text-[11px] text-slate-500 mb-1 font-semibold uppercase tracking-wider">AI Taslak Mesajı:</p>
                     <p className="text-xs text-rose-300 italic font-serif">"{action.action}"</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}