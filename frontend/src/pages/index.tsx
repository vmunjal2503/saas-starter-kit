/**
 * Landing page — SaaS Starter Kit
 */

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold">SaaS Kit</h1>
        <div className="flex gap-4">
          <a href="/login" className="px-4 py-2 text-gray-300 hover:text-white transition">
            Log in
          </a>
          <a href="/register" className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition">
            Get Started
          </a>
        </div>
      </nav>

      {/* Hero */}
      <main className="max-w-4xl mx-auto text-center px-8 py-24">
        <h2 className="text-5xl font-bold leading-tight mb-6">
          Ship your SaaS in{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
            days, not months
          </span>
        </h2>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
          Production-ready boilerplate with authentication, multi-tenancy,
          Stripe billing, and role-based access control. Start building features
          from day one.
        </p>
        <div className="flex gap-4 justify-center">
          <a href="/register" className="px-8 py-3 bg-blue-600 rounded-lg text-lg font-medium hover:bg-blue-700 transition">
            Start Free Trial
          </a>
          <a href="/docs" className="px-8 py-3 border border-gray-600 rounded-lg text-lg hover:border-gray-400 transition">
            View Docs
          </a>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24 text-left">
          {[
            { title: "Authentication", desc: "JWT + OAuth, email verification, password reset — ready out of the box." },
            { title: "Multi-Tenancy", desc: "Organization-based tenancy with invite flows and role management." },
            { title: "Stripe Billing", desc: "Subscriptions, checkout, customer portal, and webhook handling." },
            { title: "RBAC", desc: "Owner, Admin, Member, Viewer roles with granular permission checks." },
            { title: "API-First", desc: "FastAPI backend with auto-generated OpenAPI docs and type safety." },
            { title: "Deploy Ready", desc: "Docker, Terraform, and CI/CD included. Deploy to AWS in minutes." },
          ].map((feature) => (
            <div key={feature.title} className="p-6 rounded-xl bg-gray-800/50 border border-gray-700">
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-400 text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-8 text-gray-500 text-sm">
        Built by Vikas Munjal
      </footer>
    </div>
  );
}
