/**
 * Dashboard layout with sidebar navigation.
 */

import React from "react";

interface Props {
  children: React.ReactNode;
  activePage?: string;
}

const navItems = [
  { name: "Dashboard", href: "/dashboard", icon: "📊" },
  { name: "Team", href: "/dashboard/team", icon: "👥" },
  { name: "Billing", href: "/dashboard/billing", icon: "💳" },
  { name: "Settings", href: "/dashboard/settings", icon: "⚙️" },
];

export default function DashboardLayout({ children, activePage }: Props) {
  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 p-6">
        <h1 className="text-xl font-bold text-gray-900 mb-8">SaaS Kit</h1>
        <nav className="space-y-1">
          {navItems.map((item) => (
            <a
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition ${
                activePage === item.name
                  ? "bg-blue-50 text-blue-700"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <span>{item.icon}</span>
              {item.name}
            </a>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
