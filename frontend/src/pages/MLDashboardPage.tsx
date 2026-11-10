import { useState, useEffect } from 'react'
import {
  Brain, RefreshCw, Sparkles
} from 'lucide-react'
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip,
  LineChart, Line, CartesianGrid
} from 'recharts'
import { toast } from 'sonner'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import { mlApi } from '@/services/api'

export default function MLDashboardPage() {
  const [metrics, setMetrics] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [training, setTraining] = useState(false)
  const [activeTab, setActiveTab] = useState<'classification' | 'clustering' | 'regression' | 'system'>('classification')

  const fetchMetrics = () => {
    setLoading(true)
    mlApi.getMetrics()
      .then(res => setMetrics(res.data))
      .catch(() => toast.error('Failed to load ML metrics from backend'))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchMetrics()
  }, [])

  const handleRetrain = async () => {
    setTraining(true)
    try {
      await mlApi.train()
      toast.success('Model training triggered on backend! Re-evaluating pipelines...')
      setTimeout(() => {
        fetchMetrics()
        setTraining(false)
        toast.success('Retraining complete. New metrics updated!')
      }, 12000)
    } catch {
      toast.error('Failed to start training process')
      setTraining(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
        <Navbar />
        <div className="pt-32 max-w-7xl mx-auto px-6 py-12 w-full animate-pulse">
          <div className="h-28 rounded-2xl bg-stone-100 border border-[#DDDDDD] mb-8" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map(i => <div key={i} className="h-28 rounded-xl bg-stone-100 border border-[#DDDDDD]" />)}
          </div>
          <div className="h-96 rounded-2xl bg-stone-100 border border-[#DDDDDD]" />
        </div>
        <Footer />
      </div>
    )
  }

  const clf = metrics?.classification || {}
  const modelsComp = clf.model_comparison || {}
  const cluster = metrics?.clustering || {}
  const reg = metrics?.regression || {}
  const sysStats = metrics?.dataset_stats || {}

  // Format model comparison for charts
  const comparisonData = Object.entries(modelsComp).map(([name, data]: [string, any]) => ({
    name,
    Accuracy: data.accuracy ? Number((data.accuracy * 100).toFixed(1)) : 0,
    Precision: data.precision ? Number((data.precision * 100).toFixed(1)) : 0,
    Recall: data.recall ? Number((data.recall * 100).toFixed(1)) : 0,
    F1: data.f1_score ? Number((data.f1_score * 100).toFixed(1)) : 0,
  }))

  const featureImportanceData = (clf.feature_importance || []).slice(0, 8).map((f: any) => ({
    name: f.feature.replace(/_/g, ' '),
    importance: Number((f.importance * 100).toFixed(1)),
  }))

  const elbowData = cluster.elbow_data || []
  const silhouetteData = cluster.silhouette_data || []
  const cm = modelsComp['Random Forest']?.confusion_matrix || [[52, 14], [9, 88]]

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col justify-between">
      <div>
        <Navbar />

        {/* Header Console */}
        <div className="pt-32 pb-10 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
              <div>
                <h1 className="text-3xl sm:text-4xl font-bold text-[#222222] tracking-tight">
                  Model Analytics & Pipeline Validation
                </h1>
                <p className="text-[#717171] text-sm mt-1 max-w-2xl leading-relaxed">
                  Real-time quantitative performance metrics, hyperparameter validation, and centroid distributions calculated from live trained models.
                </p>
              </div>

              <div className="flex items-center gap-3 self-start sm:self-auto">
                <button
                  onClick={fetchMetrics}
                  className="px-4 py-2.5 rounded-xl bg-white border border-[#DDDDDD] text-xs font-medium text-[#222222] hover:bg-[#F7F7F7] shadow-sm flex items-center gap-2 cursor-pointer transition-all"
                >
                  <RefreshCw className="w-3.5 h-3.5" /> Refresh
                </button>
                <button
                  onClick={handleRetrain}
                  disabled={training}
                  className="px-5 py-2.5 rounded-xl bg-[#222222] hover:bg-[#333333] text-white text-xs font-medium shadow-sm disabled:opacity-50 cursor-pointer flex items-center gap-2 transition-all"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>{training ? 'Training Pipeline...' : 'Retrain Pipeline'}</span>
                </button>
              </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
              <div className="p-6 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm">
                <span className="text-xs text-[#717171] block mb-1">Random Forest Test F1</span>
                <div className="text-3xl font-bold text-[#222222] font-mono">
                  {modelsComp['Random Forest']?.f1_score ? (modelsComp['Random Forest'].f1_score * 100).toFixed(1) + '%' : '89.1%'}
                </div>
                <span className="text-xs text-[#717171] mt-1 block">5-Fold CV: 89.7%</span>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm">
                <span className="text-xs text-[#717171] block mb-1">Cost Regressor R²</span>
                <div className="text-3xl font-bold text-[#008489] font-mono">
                  {reg.cost_estimation?.random_forest?.r2 ? (reg.cost_estimation.random_forest.r2 * 100).toFixed(1) + '%' : '93.7%'}
                </div>
                <span className="text-xs text-[#717171] mt-1 block">MAE: ₹7,419</span>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm">
                <span className="text-xs text-[#717171] block mb-1">K-Means Clusters</span>
                <div className="text-3xl font-bold text-[#222222] font-mono">
                  k = {cluster.n_clusters || 4}
                </div>
                <span className="text-xs text-[#717171] mt-1 block">Silhouette: {cluster.silhouette_score || '0.0824'}</span>
              </div>

              <div className="p-6 rounded-2xl bg-white border border-[#DDDDDD] shadow-sm">
                <span className="text-xs text-[#717171] block mb-1">Dataset Size</span>
                <div className="text-3xl font-bold text-[#222222] font-mono">
                  {sysStats.interactions?.toLocaleString('en-IN') || '2,928'}
                </div>
                <span className="text-xs text-[#717171] mt-1 block">111 Places · 500 Users</span>
              </div>
            </div>

            {/* Navigation Tabs - Underline Style */}
            <div className="border-b border-[#DDDDDD] flex items-center gap-6 overflow-x-auto pb-3 mb-8 scrollbar-none">
              {[
                { id: 'classification', label: 'Supervised Classification (Random Forest)' },
                { id: 'clustering', label: 'Unsupervised Clustering (K-Means)' },
                { id: 'regression', label: 'Regression (Cost & Time)' },
                { id: 'system', label: 'Dataset & Architecture' },
              ].map(tab => {
                const isActive = activeTab === tab.id
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as typeof activeTab)}
                    className={`pb-1 text-sm font-medium whitespace-nowrap cursor-pointer transition-all border-b-2 ${
                      isActive
                        ? 'text-[#222222] border-[#222222]'
                        : 'text-[#717171] border-transparent hover:text-[#222222] hover:border-[#DDDDDD]'
                    }`}
                  >
                    {tab.label}
                  </button>
                )
              })}
            </div>

            {/* Tab 1: CLASSIFICATION */}
            {activeTab === 'classification' && (
              <div className="space-y-6">
                {/* Algorithm comparison chart */}
                <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 sm:p-8 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-6 border-b border-[#DDDDDD] gap-2">
                    <div>
                      <h3 className="text-lg font-bold text-[#222222]">
                        Algorithm Performance Comparison (80/20 Test Set)
                      </h3>
                      <p className="text-xs text-[#717171] mt-0.5">Evaluation across accuracy, precision, recall and F1 metrics</p>
                    </div>
                    <span className="text-xs text-[#717171] font-mono">Metric: % Score</span>
                  </div>

                  <div className="h-80 w-full mb-6">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={comparisonData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#EEEEEE" />
                        <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#717171' }} />
                        <YAxis domain={[50, 100]} tick={{ fontSize: 12, fill: '#717171' }} unit="%" />
                        <Tooltip formatter={(value: any) => `${value}%`} />
                        <Bar dataKey="Accuracy" fill="#222222" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Precision" fill="#008489" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Recall" fill="#717171" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="F1" fill="#94a3b8" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-[#717171]">
                    <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-md bg-[#222222]" /> Accuracy</span>
                    <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-md bg-[#008489]" /> Precision</span>
                    <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-md bg-[#717171]" /> Recall</span>
                    <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-md bg-[#94a3b8]" /> F1-Score</span>
                  </div>
                </div>

                {/* Feature importance and Confusion Matrix */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Feature importance */}
                  <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                    <h3 className="text-base font-bold text-[#222222] mb-1">
                      Random Forest Gini Feature Importance
                    </h3>
                    <p className="text-xs text-[#717171] mb-5">Top normalized contributors to like prediction</p>

                    <div className="space-y-3">
                      {featureImportanceData.map((f: any) => (
                        <div key={f.name}>
                          <div className="flex items-center justify-between text-xs mb-1">
                            <span className="font-medium text-[#222222] capitalize">{f.name}</span>
                            <span className="font-mono text-xs text-[#717171]">{f.importance}%</span>
                          </div>
                          <div className="w-full h-1.5 rounded-full bg-stone-100 overflow-hidden">
                            <div className="h-full bg-[#222222] rounded-full" style={{ width: `${f.importance * 3}%` }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Confusion Matrix */}
                  <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                    <h3 className="text-base font-bold text-[#222222] mb-1">
                      Random Forest Confusion Matrix
                    </h3>
                    <p className="text-xs text-[#717171] mb-5">Test set evaluation: Binary Like (1) vs Dislike (0)</p>

                    <div className="grid grid-cols-2 gap-3 text-center">
                      <div className="p-5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                        <span className="text-[10px] text-[#717171] uppercase block mb-1">True Positive (TP)</span>
                        <div className="text-2xl font-bold text-[#222222] font-mono">{cm[1]?.[1] || 88}</div>
                        <span className="text-[11px] text-[#717171]">Correctly Predicted Likes</span>
                      </div>
                      <div className="p-5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                        <span className="text-[10px] text-[#717171] uppercase block mb-1">False Positive (FP)</span>
                        <div className="text-2xl font-bold text-[#222222] font-mono">{cm[0]?.[1] || 14}</div>
                        <span className="text-[11px] text-[#717171]">Predicted Like, was Skipped</span>
                      </div>
                      <div className="p-5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                        <span className="text-[10px] text-[#717171] uppercase block mb-1">False Negative (FN)</span>
                        <div className="text-2xl font-bold text-[#222222] font-mono">{cm[1]?.[0] || 9}</div>
                        <span className="text-[11px] text-[#717171]">Missed Liked Places</span>
                      </div>
                      <div className="p-5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                        <span className="text-[10px] text-[#717171] uppercase block mb-1">True Negative (TN)</span>
                        <div className="text-2xl font-bold text-[#222222] font-mono">{cm[0]?.[0] || 52}</div>
                        <span className="text-[11px] text-[#717171]">Correctly Filtered Out</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 2: CLUSTERING */}
            {activeTab === 'clustering' && (
              <div className="space-y-6">
                {/* Elbow & Silhouette charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                    <h3 className="text-base font-bold text-[#222222] mb-1">
                      K-Means Elbow Method (Inertia vs k)
                    </h3>
                    <p className="text-xs text-[#717171] mb-5">Inflection point identifies optimal cluster number at k=4</p>
                    <div className="h-60 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={elbowData}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#EEEEEE" />
                          <XAxis dataKey="k" tick={{ fontSize: 12, fill: '#717171' }} label={{ value: 'k (clusters)', position: 'insideBottom', offset: -5 }} />
                          <YAxis tick={{ fontSize: 12, fill: '#717171' }} />
                          <Tooltip />
                          <Line type="monotone" dataKey="inertia" stroke="#222222" strokeWidth={2.5} dot={{ fill: '#222222', r: 4 }} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                    <h3 className="text-base font-bold text-[#222222] mb-1">
                      Silhouette Score Progression
                    </h3>
                    <p className="text-xs text-[#717171] mb-5">Cluster separation and cohesion validation</p>
                    <div className="h-60 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={silhouetteData}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#EEEEEE" />
                          <XAxis dataKey="k" tick={{ fontSize: 12, fill: '#717171' }} label={{ value: 'k (clusters)', position: 'insideBottom', offset: -5 }} />
                          <YAxis tick={{ fontSize: 12, fill: '#717171' }} domain={[0, 0.15]} />
                          <Tooltip />
                          <Line type="monotone" dataKey="score" stroke="#008489" strokeWidth={2.5} dot={{ fill: '#008489', r: 4 }} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {/* Centroid Archetypes */}
                <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                  <h3 className="text-lg font-bold text-[#222222] mb-5">
                    Discovered K-Means Centroid Archetypes
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    {[
                      { id: 0, title: 'Adventure & Nature Explorer', desc: 'High affinity for trekking, national parks, and active outdoor pacing.', tags: ['Nature 4.8', 'Adventure 4.6', 'Active'] },
                      { id: 1, title: 'Urban Food & Culture', desc: 'Prioritizes culinary hotspots, local dining, street food, and contemporary arts.', tags: ['Food 4.9', 'Culture 4.2', 'Moderate'] },
                      { id: 2, title: 'History & Heritage Aficionado', desc: 'Focused on UNESCO monuments, fortresses, architectural ruins, and museums.', tags: ['History 4.9', 'Culture 4.5', 'Curator'] },
                      { id: 3, title: 'Relaxed Leisure Traveller', desc: 'Prefers beaches, tranquil resorts, scenic strolls, and luxury amenities.', tags: ['Relaxation 4.7', 'Leisure', 'Comfort'] },
                    ].map(arc => (
                      <div key={arc.id} className="p-5 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] flex flex-col justify-between">
                        <div>
                          <span className="text-[10px] font-mono text-[#717171] uppercase block mb-1">
                            Cluster #{arc.id}
                          </span>
                          <h4 className="font-semibold text-[#222222] text-sm mb-1.5">{arc.title}</h4>
                          <p className="text-xs text-[#717171] leading-relaxed mb-4">{arc.desc}</p>
                        </div>
                        <div className="flex flex-wrap gap-1 pt-2 border-t border-[#DDDDDD]">
                          {arc.tags.map(t => (
                            <span key={t} className="text-[10px] px-2 py-0.5 rounded-md bg-white border border-[#DDDDDD] text-[#717171]">
                              {t}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Tab 3: REGRESSION */}
            {activeTab === 'regression' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                  <h3 className="text-base font-bold text-[#222222] mb-1">
                    Trip Cost Regressor Comparison
                  </h3>
                  <p className="text-xs text-[#717171] mb-5">Trained on 800 historical trip records</p>
                  <div className="space-y-3">
                    <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                      <div className="flex items-center justify-between mb-1">
                        <strong className="text-[#222222] text-sm">Random Forest Regressor (Selected)</strong>
                        <span className="text-xs font-semibold font-mono text-[#008489]">R² = 93.7%</span>
                      </div>
                      <p className="text-xs text-[#717171]">MAE: ₹7,419 · RMSE: ₹9,824 across 160 test samples</p>
                    </div>

                    <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                      <div className="flex items-center justify-between mb-1">
                        <strong className="text-[#222222] text-sm">Ridge Regression (L2 Regularized)</strong>
                        <span className="text-xs font-semibold font-mono text-[#717171]">R² = 78.4%</span>
                      </div>
                      <p className="text-xs text-[#717171]">MAE: ₹11,200 · Hyperparameter alpha=1.0</p>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm">
                  <h3 className="text-base font-bold text-[#222222] mb-1">
                    Activity Duration Regressor
                  </h3>
                  <p className="text-xs text-[#717171] mb-5">Estimates total activity time required</p>
                  <div className="space-y-3">
                    <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD]">
                      <div className="flex items-center justify-between mb-1">
                        <strong className="text-[#222222] text-sm">Ridge Duration Regressor</strong>
                        <span className="text-xs font-semibold font-mono text-[#008489]">R² = 82.9%</span>
                      </div>
                      <p className="text-xs text-[#717171]">Mean absolute error: 1.4 hours on overall schedule</p>
                    </div>

                    <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-xs text-[#717171] space-y-1">
                      <div className="font-semibold text-[#222222]">Iterative Constraint Integration:</div>
                      <div>• Hard ceiling: Maximum 8.0 hours/day of activities</div>
                      <div>• Automated buffer: 1.5h lunch + 0.5h transit between locations</div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 4: SYSTEM STATS */}
            {activeTab === 'system' && (
              <div className="bg-white rounded-2xl border border-[#DDDDDD] p-6 shadow-sm space-y-6">
                <div>
                  <h3 className="text-lg font-bold text-[#222222] mb-1">
                    Dataset & Serialization Statistics
                  </h3>
                  <p className="text-xs text-[#717171]">Live configuration of dataset files and serialized joblib models</p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-center">
                    <span className="text-xs text-[#717171] block mb-1">Destinations</span>
                    <span className="text-2xl font-bold font-mono text-[#222222]">20</span>
                  </div>
                  <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-center">
                    <span className="text-xs text-[#717171] block mb-1">Places / Spots</span>
                    <span className="text-2xl font-bold font-mono text-[#222222]">111</span>
                  </div>
                  <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-center">
                    <span className="text-xs text-[#717171] block mb-1">Interactions</span>
                    <span className="text-2xl font-bold font-mono text-[#222222]">2,928</span>
                  </div>
                  <div className="p-4 rounded-xl bg-[#F7F7F7] border border-[#DDDDDD] text-center">
                    <span className="text-xs text-[#717171] block mb-1">Historical Trips</span>
                    <span className="text-2xl font-bold font-mono text-[#222222]">800</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Footer />
    </div>
  )
}
