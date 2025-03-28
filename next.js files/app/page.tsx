import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
              <span className="text-white font-bold text-lg">H</span>
            </div>
            <h1 className="text-xl font-bold text-gray-800">MediSync</h1>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/auth/login">
              <Button variant="outline">Login</Button>
            </Link>
            <Link href="/auth/register">
              <Button>Register</Button>
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="py-16 px-4">
          <div className="container mx-auto max-w-6xl">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                  Modern Healthcare Management System
                </h1>
                <p className="text-lg text-gray-600 mb-8">
                  Streamline your hospital operations with our comprehensive
                  management system. Designed for administrators, doctors, and
                  patients.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link href="/auth/register">
                    <Button size="lg" className="w-full sm:w-auto">
                      Get Started
                    </Button>
                  </Link>
                  <Link href="/about">
                    <Button
                      size="lg"
                      variant="outline"
                      className="w-full sm:w-auto"
                    >
                      Learn More
                    </Button>
                  </Link>
                </div>
              </div>
              <div className="relative">
                <div className="absolute -top-6 -left-6 w-24 h-24 bg-blue-100 rounded-full z-0"></div>
                <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-blue-50 rounded-full z-0"></div>
                <div className="relative z-10 bg-white p-6 rounded-xl shadow-lg">
                  <img
                    src="/placeholder.svg?height=400&width=500"
                    alt="Hospital Management Dashboard"
                    className="w-full rounded-lg"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-16 px-4 bg-gray-50">
          <div className="container mx-auto max-w-6xl">
            <h2 className="text-3xl font-bold text-center mb-12">
              Key Features
            </h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  title: "For Administrators",
                  description:
                    "Manage staff, monitor operations, and optimize resource allocation.",
                  icon: "LayoutDashboard",
                },
                {
                  title: "For Doctors",
                  description:
                    "Access patient records, manage appointments, and track treatment plans.",
                  icon: "Stethoscope",
                },
                {
                  title: "For Patients",
                  description:
                    "Book appointments, view medical history, and communicate with doctors.",
                  icon: "User",
                },
              ].map((feature, index) => (
                <div
                  key={index}
                  className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <span className="text-blue-600 text-xl">
                      {feature.icon === "LayoutDashboard" && "📊"}
                      {feature.icon === "Stethoscope" && "👨‍⚕️"}
                      {feature.icon === "User" && "👤"}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-800 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                  <span className="text-white font-bold text-lg">H</span>
                </div>
                <h2 className="text-xl font-bold">MediSync</h2>
              </div>
              <p className="text-gray-400">
                Modern healthcare management system for hospitals and clinics.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Home
                  </Link>
                </li>
                <li>
                  <Link
                    href="/about"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    About
                  </Link>
                </li>
                <li>
                  <Link
                    href="/features"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Features
                  </Link>
                </li>
                <li>
                  <Link
                    href="/contact"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Legal</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/privacy"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link
                    href="/terms"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact</h3>
              <p className="text-gray-400 mb-2">info@medicare.com</p>
              <p className="text-gray-400">+1 (555) 123-4567</p>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>© {new Date().getFullYear()} MediSync. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
