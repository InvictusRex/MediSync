import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Search } from "lucide-react";

// Sample data
const doctors = [
  {
    id: "D001",
    name: "Dr. Sarah Johnson",
    department: "Cardiology",
    specialization: "Heart Disease",
    experience: "15 years",
    contact: "+1 (555) 123-4567",
    email: "sarah.johnson@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D002",
    name: "Dr. Michael Chen",
    department: "Neurology",
    specialization: "Brain Disorders",
    experience: "12 years",
    contact: "+1 (555) 234-5678",
    email: "michael.chen@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D003",
    name: "Dr. Emily Rodriguez",
    department: "Pediatrics",
    specialization: "Child Healthcare",
    experience: "10 years",
    contact: "+1 (555) 345-6789",
    email: "emily.rodriguez@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D004",
    name: "Dr. James Wilson",
    department: "Orthopedics",
    specialization: "Bone & Joint Surgery",
    experience: "18 years",
    contact: "+1 (555) 456-7890",
    email: "james.wilson@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D005",
    name: "Dr. Olivia Thompson",
    department: "Dermatology",
    specialization: "Skin Conditions",
    experience: "8 years",
    contact: "+1 (555) 567-8901",
    email: "olivia.thompson@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D006",
    name: "Dr. Robert Garcia",
    department: "Oncology",
    specialization: "Cancer Treatment",
    experience: "20 years",
    contact: "+1 (555) 678-9012",
    email: "robert.garcia@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D007",
    name: "Dr. Jennifer Lee",
    department: "Psychiatry",
    specialization: "Mental Health",
    experience: "14 years",
    contact: "+1 (555) 789-0123",
    email: "jennifer.lee@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
  {
    id: "D008",
    name: "Dr. David Kim",
    department: "Ophthalmology",
    specialization: "Eye Care",
    experience: "16 years",
    contact: "+1 (555) 890-1234",
    email: "david.kim@medicare.com",
    image: "/placeholder.svg?height=150&width=150",
  },
];

const departments = [
  "All Departments",
  "Cardiology",
  "Neurology",
  "Pediatrics",
  "Orthopedics",
  "Dermatology",
  "Oncology",
  "Psychiatry",
  "Ophthalmology",
];

export default function DoctorsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Link href="/" className="flex items-center space-x-2">
              <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                <span className="text-white font-bold text-lg">H</span>
              </div>
              <h1 className="text-xl font-bold text-gray-800">MediSync</h1>
            </Link>
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

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-4">Our Doctors</h1>
          <p className="text-gray-600 max-w-3xl">
            Meet our team of experienced and dedicated healthcare professionals.
            Our doctors are committed to providing the highest quality of care
            to all our patients.
          </p>
        </div>

        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="relative flex-grow">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              type="search"
              placeholder="Search doctors by name or specialization..."
              className="pl-10"
            />
          </div>
          <div className="w-full md:w-64">
            <Select defaultValue="All Departments">
              <SelectTrigger>
                <SelectValue placeholder="Filter by department" />
              </SelectTrigger>
              <SelectContent>
                {departments.map((department) => (
                  <SelectItem key={department} value={department}>
                    {department}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {doctors.map((doctor) => (
            <Card
              key={doctor.id}
              className="overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="aspect-square bg-gray-100 flex items-center justify-center">
                <img
                  src={doctor.image || "/placeholder.svg"}
                  alt={doctor.name}
                  className="object-cover w-full h-full"
                />
              </div>
              <CardContent className="p-4">
                <h3 className="font-bold text-lg mb-1">{doctor.name}</h3>
                <p className="text-blue-600 font-medium mb-2">
                  {doctor.department}
                </p>
                <div className="space-y-2 text-sm text-gray-600">
                  <p>
                    <span className="font-medium">Specialization:</span>{" "}
                    {doctor.specialization}
                  </p>
                  <p>
                    <span className="font-medium">Experience:</span>{" "}
                    {doctor.experience}
                  </p>
                  <p>
                    <span className="font-medium">Contact:</span>{" "}
                    {doctor.contact}
                  </p>
                  <p>
                    <span className="font-medium">Email:</span> {doctor.email}
                  </p>
                </div>
                <div className="mt-4">
                  <Link href="/auth/login">
                    <Button className="w-full">Book Appointment</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>

      <footer className="bg-gray-800 text-white py-12 mt-12">
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
                    href="/doctors"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Doctors
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
