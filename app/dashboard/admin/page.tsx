"use client"

import { useState } from "react"
import DashboardLayout from "@/components/dashboard-layout"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { PlusCircle, Search, UserPlus, Users } from "lucide-react"

// Sample data
const initialDoctors = [
  {
    id: "D001",
    name: "Dr. Sarah Johnson",
    department: "Cardiology",
    contact: "+1 (555) 123-4567",
    email: "sarah.johnson@medicare.com",
  },
  {
    id: "D002",
    name: "Dr. Michael Chen",
    department: "Neurology",
    contact: "+1 (555) 234-5678",
    email: "michael.chen@medicare.com",
  },
  {
    id: "D003",
    name: "Dr. Emily Rodriguez",
    department: "Pediatrics",
    contact: "+1 (555) 345-6789",
    email: "emily.rodriguez@medicare.com",
  },
  {
    id: "D004",
    name: "Dr. James Wilson",
    department: "Orthopedics",
    contact: "+1 (555) 456-7890",
    email: "james.wilson@medicare.com",
  },
  {
    id: "D005",
    name: "Dr. Olivia Thompson",
    department: "Dermatology",
    contact: "+1 (555) 567-8901",
    email: "olivia.thompson@medicare.com",
  },
]

const initialPatients = [
  {
    id: "P001",
    name: "John Smith",
    age: 45,
    bloodGroup: "O+",
    contact: "+1 (555) 987-6543",
    email: "john.smith@example.com",
  },
  {
    id: "P002",
    name: "Emma Davis",
    age: 32,
    bloodGroup: "A-",
    contact: "+1 (555) 876-5432",
    email: "emma.davis@example.com",
  },
  {
    id: "P003",
    name: "Robert Johnson",
    age: 58,
    bloodGroup: "B+",
    contact: "+1 (555) 765-4321",
    email: "robert.johnson@example.com",
  },
  {
    id: "P004",
    name: "Sophia Martinez",
    age: 27,
    bloodGroup: "AB+",
    contact: "+1 (555) 654-3210",
    email: "sophia.martinez@example.com",
  },
  {
    id: "P005",
    name: "William Brown",
    age: 63,
    bloodGroup: "A+",
    contact: "+1 (555) 543-2109",
    email: "william.brown@example.com",
  },
]

export default function AdminDashboard() {
  const [doctors, setDoctors] = useState(initialDoctors)
  const [patients, setPatients] = useState(initialPatients)
  const [searchTerm, setSearchTerm] = useState("")
  const [isAddDoctorOpen, setIsAddDoctorOpen] = useState(false)
  const [newDoctor, setNewDoctor] = useState({
    name: "",
    department: "",
    contact: "",
    email: "",
  })

  const handleAddDoctor = () => {
    const newId = `D${(doctors.length + 1).toString().padStart(3, "0")}`
    setDoctors([...doctors, { id: newId, ...newDoctor }])
    setNewDoctor({ name: "", department: "", contact: "", email: "" })
    setIsAddDoctorOpen(false)
  }

  const handleRemoveDoctor = (id: string) => {
    setDoctors(doctors.filter((doctor) => doctor.id !== id))
  }

  const filteredDoctors = doctors.filter(
    (doctor) =>
      doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doctor.department.toLowerCase().includes(searchTerm.toLowerCase()) ||
      doctor.id.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const filteredPatients = patients.filter(
    (patient) =>
      patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.id.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
            <p className="text-muted-foreground">Manage doctors, patients, and hospital operations</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search..."
                className="w-full md:w-[200px] pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <Dialog open={isAddDoctorOpen} onOpenChange={setIsAddDoctorOpen}>
              <DialogTrigger asChild>
                <Button>
                  <UserPlus className="mr-2 h-4 w-4" />
                  Add Doctor
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add New Doctor</DialogTitle>
                  <DialogDescription>Enter the details of the new doctor to add them to the system.</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Full Name</Label>
                    <Input
                      id="name"
                      value={newDoctor.name}
                      onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
                      placeholder="Dr. Jane Doe"
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="department">Department</Label>
                    <Select
                      onValueChange={(value) => setNewDoctor({ ...newDoctor, department: value })}
                      value={newDoctor.department}
                    >
                      <SelectTrigger id="department">
                        <SelectValue placeholder="Select department" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Cardiology">Cardiology</SelectItem>
                        <SelectItem value="Neurology">Neurology</SelectItem>
                        <SelectItem value="Pediatrics">Pediatrics</SelectItem>
                        <SelectItem value="Orthopedics">Orthopedics</SelectItem>
                        <SelectItem value="Dermatology">Dermatology</SelectItem>
                        <SelectItem value="Oncology">Oncology</SelectItem>
                        <SelectItem value="Psychiatry">Psychiatry</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="contact">Contact Number</Label>
                    <Input
                      id="contact"
                      value={newDoctor.contact}
                      onChange={(e) => setNewDoctor({ ...newDoctor, contact: e.target.value })}
                      placeholder="+1 (555) 123-4567"
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={newDoctor.email}
                      onChange={(e) => setNewDoctor({ ...newDoctor, email: e.target.value })}
                      placeholder="doctor@medicare.com"
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button variant="outline" onClick={() => setIsAddDoctorOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleAddDoctor}>Add Doctor</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Doctors</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{doctors.length}</div>
              <p className="text-xs text-muted-foreground">
                Across {new Set(doctors.map((d) => d.department)).size} departments
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Patients</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{patients.length}</div>
              <p className="text-xs text-muted-foreground">Active patient records</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Appointments Today</CardTitle>
              <PlusCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">24</div>
              <p className="text-xs text-muted-foreground">Scheduled for today</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">New Registrations</CardTitle>
              <UserPlus className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground">New patients this week</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="doctors" className="w-full">
          <TabsList>
            <TabsTrigger value="doctors">Doctors</TabsTrigger>
            <TabsTrigger value="patients">Patients</TabsTrigger>
          </TabsList>
          <TabsContent value="doctors" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Doctors Management</CardTitle>
                <CardDescription>View and manage all doctors in the system</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Name</TableHead>
                      <TableHead>Department</TableHead>
                      <TableHead>Contact</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredDoctors.map((doctor) => (
                      <TableRow key={doctor.id}>
                        <TableCell className="font-medium">{doctor.id}</TableCell>
                        <TableCell>{doctor.name}</TableCell>
                        <TableCell>{doctor.department}</TableCell>
                        <TableCell>{doctor.contact}</TableCell>
                        <TableCell>{doctor.email}</TableCell>
                        <TableCell className="text-right">
                          <Button variant="destructive" size="sm" onClick={() => handleRemoveDoctor(doctor.id)}>
                            Remove
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="patients" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Patients Management</CardTitle>
                <CardDescription>View all registered patients in the system</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Name</TableHead>
                      <TableHead>Age</TableHead>
                      <TableHead>Blood Group</TableHead>
                      <TableHead>Contact</TableHead>
                      <TableHead>Email</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredPatients.map((patient) => (
                      <TableRow key={patient.id}>
                        <TableCell className="font-medium">{patient.id}</TableCell>
                        <TableCell>{patient.name}</TableCell>
                        <TableCell>{patient.age}</TableCell>
                        <TableCell>{patient.bloodGroup}</TableCell>
                        <TableCell>{patient.contact}</TableCell>
                        <TableCell>{patient.email}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}

