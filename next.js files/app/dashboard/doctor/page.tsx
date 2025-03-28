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
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Calendar, Clock, Search, User } from "lucide-react"

// Sample data
const initialPatients = [
  {
    id: "P001",
    name: "John Smith",
    age: 45,
    bloodGroup: "O+",
    contact: "+1 (555) 987-6543",
    medicalHistory: "Hypertension, Cholesterol",
  },
  {
    id: "P002",
    name: "Emma Davis",
    age: 32,
    bloodGroup: "A-",
    contact: "+1 (555) 876-5432",
    medicalHistory: "Asthma",
  },
  {
    id: "P003",
    name: "Robert Johnson",
    age: 58,
    bloodGroup: "B+",
    contact: "+1 (555) 765-4321",
    medicalHistory: "Diabetes Type 2, Arthritis",
  },
  {
    id: "P004",
    name: "Sophia Martinez",
    age: 27,
    bloodGroup: "AB+",
    contact: "+1 (555) 654-3210",
    medicalHistory: "Allergies (Peanuts, Penicillin)",
  },
  {
    id: "P005",
    name: "William Brown",
    age: 63,
    bloodGroup: "A+",
    contact: "+1 (555) 543-2109",
    medicalHistory: "Heart Disease, High Blood Pressure",
  },
]

const initialAppointments = [
  {
    id: "A001",
    patientId: "P001",
    patientName: "John Smith",
    date: "2025-03-29",
    time: "09:00 AM",
    reason: "Follow-up on blood pressure medication",
  },
  {
    id: "A002",
    patientId: "P003",
    patientName: "Robert Johnson",
    date: "2025-03-29",
    time: "10:30 AM",
    reason: "Diabetes check-up",
  },
  {
    id: "A003",
    patientId: "P002",
    patientName: "Emma Davis",
    date: "2025-03-29",
    time: "01:15 PM",
    reason: "Asthma treatment review",
  },
  {
    id: "A004",
    patientId: "P005",
    patientName: "William Brown",
    date: "2025-03-30",
    time: "11:00 AM",
    reason: "Cardiac evaluation",
  },
  {
    id: "A005",
    patientId: "P004",
    patientName: "Sophia Martinez",
    date: "2025-03-30",
    time: "03:45 PM",
    reason: "Allergy consultation",
  },
]

export default function DoctorDashboard() {
  const [patients, setPatients] = useState(initialPatients)
  const [appointments, setAppointments] = useState(initialAppointments)
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedPatient, setSelectedPatient] = useState<any>(null)
  const [isUpdateOpen, setIsUpdateOpen] = useState(false)
  const [updatedHistory, setUpdatedHistory] = useState("")

  const handleUpdateHistory = () => {
    setPatients(
      patients.map((patient) =>
        patient.id === selectedPatient.id ? { ...patient, medicalHistory: updatedHistory } : patient,
      ),
    )
    setIsUpdateOpen(false)
  }

  const openUpdateDialog = (patient: any) => {
    setSelectedPatient(patient)
    setUpdatedHistory(patient.medicalHistory)
    setIsUpdateOpen(true)
  }

  const filteredPatients = patients.filter(
    (patient) =>
      patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.id.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const filteredAppointments = appointments.filter(
    (appointment) =>
      appointment.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      appointment.patientId.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  const todayAppointments = appointments.filter((appointment) => appointment.date === "2025-03-29")

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Doctor Dashboard</h1>
            <p className="text-muted-foreground">Manage your patients and appointments</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search patients..."
                className="w-full md:w-[200px] pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Patients</CardTitle>
              <User className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{patients.length}</div>
              <p className="text-xs text-muted-foreground">Assigned to you</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Today's Appointments</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{todayAppointments.length}</div>
              <p className="text-xs text-muted-foreground">Scheduled for today</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Next Appointment</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {todayAppointments.length > 0 ? todayAppointments[0].time : "No appointments"}
              </div>
              <p className="text-xs text-muted-foreground">
                {todayAppointments.length > 0 ? `With ${todayAppointments[0].patientName}` : "Schedule empty for today"}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Appointments</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{appointments.length}</div>
              <p className="text-xs text-muted-foreground">Upcoming appointments</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="patients" className="w-full">
          <TabsList>
            <TabsTrigger value="patients">My Patients</TabsTrigger>
            <TabsTrigger value="appointments">Appointments</TabsTrigger>
          </TabsList>
          <TabsContent value="patients" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Patient Records</CardTitle>
                <CardDescription>View and update medical history for your patients</CardDescription>
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
                      <TableHead>Medical History</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
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
                        <TableCell className="max-w-[200px] truncate">
                          {patient.medicalHistory || "No history recorded"}
                        </TableCell>
                        <TableCell className="text-right">
                          <Button variant="outline" size="sm" onClick={() => openUpdateDialog(patient)}>
                            Update History
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="appointments" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Upcoming Appointments</CardTitle>
                <CardDescription>View all scheduled appointments with your patients</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Patient</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Time</TableHead>
                      <TableHead>Reason</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredAppointments.map((appointment) => (
                      <TableRow key={appointment.id}>
                        <TableCell className="font-medium">{appointment.id}</TableCell>
                        <TableCell>
                          {appointment.patientName} ({appointment.patientId})
                        </TableCell>
                        <TableCell>{appointment.date}</TableCell>
                        <TableCell>{appointment.time}</TableCell>
                        <TableCell className="max-w-[300px]">{appointment.reason}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      <Dialog open={isUpdateOpen} onOpenChange={setIsUpdateOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Update Medical History</DialogTitle>
            <DialogDescription>
              {selectedPatient && `Update medical history for ${selectedPatient.name}`}
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="medicalHistory">Medical History</Label>
              <Textarea
                id="medicalHistory"
                value={updatedHistory}
                onChange={(e) => setUpdatedHistory(e.target.value)}
                placeholder="Enter patient's medical history"
                className="h-32"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsUpdateOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdateHistory}>Update History</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </DashboardLayout>
  )
}

