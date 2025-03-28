"use client";

import { useState } from "react";
import DashboardLayout from "@/components/dashboard-layout";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Calendar, CalendarIcon, Clock, FileText, Plus } from "lucide-react";
import { format } from "date-fns";
import { Calendar as CalendarComponent } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";

// Sample data
const patientInfo = {
  id: "P001",
  name: "John Smith",
  age: 45,
  bloodGroup: "O+",
  contact: "+1 (555) 987-6543",
  email: "john.smith@example.com",
  medicalHistory: "Hypertension, High Cholesterol",
};

const initialAppointments = [
  {
    id: "A001",
    doctorName: "Dr. Sarah Johnson",
    department: "Cardiology",
    date: "2025-03-29",
    time: "09:00 AM",
    status: "Confirmed",
  },
  {
    id: "A002",
    doctorName: "Dr. Michael Chen",
    department: "Neurology",
    date: "2025-04-05",
    time: "02:30 PM",
    status: "Pending",
  },
];

const doctors = [
  { id: "D001", name: "Dr. Sarah Johnson", department: "Cardiology" },
  { id: "D002", name: "Dr. Michael Chen", department: "Neurology" },
  { id: "D003", name: "Dr. Emily Rodriguez", department: "Pediatrics" },
  { id: "D004", name: "Dr. James Wilson", department: "Orthopedics" },
  { id: "D005", name: "Dr. Olivia Thompson", department: "Dermatology" },
];

export default function PatientDashboard() {
  const [appointments, setAppointments] = useState(initialAppointments);
  const [isBookingOpen, setIsBookingOpen] = useState(false);
  const [date, setDate] = useState<Date>();
  const [newAppointment, setNewAppointment] = useState({
    doctorId: "",
    reason: "",
    time: "",
  });

  const handleBookAppointment = () => {
    if (!date || !newAppointment.doctorId || !newAppointment.time) return;

    const selectedDoctor = doctors.find(
      (d) => d.id === newAppointment.doctorId
    );
    if (!selectedDoctor) return;

    const newId = `A${(appointments.length + 1).toString().padStart(3, "0")}`;
    const formattedDate = format(date, "yyyy-MM-dd");

    setAppointments([
      ...appointments,
      {
        id: newId,
        doctorName: selectedDoctor.name,
        department: selectedDoctor.department,
        date: formattedDate,
        time: newAppointment.time,
        status: "Pending",
      },
    ]);

    setNewAppointment({ doctorId: "", reason: "", time: "" });
    setDate(undefined);
    setIsBookingOpen(false);
  };

  const handleCancelAppointment = (id: string) => {
    setAppointments(
      appointments.filter((appointment) => appointment.id !== id)
    );
  };

  const upcomingAppointments = appointments.filter(
    (appointment) => new Date(appointment.date) >= new Date()
  );

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              Patient Dashboard
            </h1>
            <p className="text-muted-foreground">
              Welcome back, {patientInfo.name}
            </p>
          </div>
          <Dialog open={isBookingOpen} onOpenChange={setIsBookingOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Book Appointment
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Book New Appointment</DialogTitle>
                <DialogDescription>
                  Fill in the details to schedule an appointment with a doctor.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2">
                  <Label htmlFor="doctor">Select Doctor</Label>
                  <Select
                    onValueChange={(value) =>
                      setNewAppointment({ ...newAppointment, doctorId: value })
                    }
                    value={newAppointment.doctorId}
                  >
                    <SelectTrigger id="doctor">
                      <SelectValue placeholder="Select a doctor" />
                    </SelectTrigger>
                    <SelectContent>
                      {doctors.map((doctor) => (
                        <SelectItem key={doctor.id} value={doctor.id}>
                          {doctor.name} - {doctor.department}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="date">Appointment Date</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant={"outline"}
                        className={cn(
                          "w-full justify-start text-left font-normal",
                          !date && "text-muted-foreground"
                        )}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date ? format(date, "PPP") : "Select a date"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <CalendarComponent
                        mode="single"
                        selected={date}
                        onSelect={setDate}
                        initialFocus
                        disabled={(date) => date < new Date()}
                      />
                    </PopoverContent>
                  </Popover>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="time">Appointment Time</Label>
                  <Select
                    onValueChange={(value) =>
                      setNewAppointment({ ...newAppointment, time: value })
                    }
                    value={newAppointment.time}
                  >
                    <SelectTrigger id="time">
                      <SelectValue placeholder="Select a time" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="09:00 AM">09:00 AM</SelectItem>
                      <SelectItem value="10:00 AM">10:00 AM</SelectItem>
                      <SelectItem value="11:00 AM">11:00 AM</SelectItem>
                      <SelectItem value="01:00 PM">01:00 PM</SelectItem>
                      <SelectItem value="02:00 PM">02:00 PM</SelectItem>
                      <SelectItem value="03:00 PM">03:00 PM</SelectItem>
                      <SelectItem value="04:00 PM">04:00 PM</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="reason">Reason for Visit</Label>
                  <Textarea
                    id="reason"
                    value={newAppointment.reason}
                    onChange={(e) =>
                      setNewAppointment({
                        ...newAppointment,
                        reason: e.target.value,
                      })
                    }
                    placeholder="Briefly describe your symptoms or reason for the appointment"
                  />
                </div>
              </div>
              <DialogFooter>
                <Button
                  variant="outline"
                  onClick={() => setIsBookingOpen(false)}
                >
                  Cancel
                </Button>
                <Button onClick={handleBookAppointment}>
                  Book Appointment
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Patient ID</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{patientInfo.id}</div>
              <p className="text-xs text-muted-foreground">
                Your unique identifier
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Blood Group</CardTitle>
              <div className="h-4 w-4 rounded-full bg-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{patientInfo.bloodGroup}</div>
              <p className="text-xs text-muted-foreground">Your blood type</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Upcoming Appointments
              </CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {upcomingAppointments.length}
              </div>
              <p className="text-xs text-muted-foreground">
                Scheduled appointments
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Next Appointment
              </CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {upcomingAppointments.length > 0
                  ? format(new Date(upcomingAppointments[0].date), "MMM d")
                  : "None"}
              </div>
              <p className="text-xs text-muted-foreground">
                {upcomingAppointments.length > 0
                  ? `${upcomingAppointments[0].time} with ${upcomingAppointments[0].doctorName}`
                  : "No upcoming appointments"}
              </p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="appointments" className="w-full">
          <TabsList>
            <TabsTrigger value="appointments">My Appointments</TabsTrigger>
            <TabsTrigger value="medical-history">Medical History</TabsTrigger>
          </TabsList>
          <TabsContent value="appointments" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Appointments</CardTitle>
                <CardDescription>
                  View and manage your scheduled appointments
                </CardDescription>
              </CardHeader>
              <CardContent>
                {appointments.length > 0 ? (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Doctor</TableHead>
                        <TableHead>Department</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead>Time</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {appointments.map((appointment) => (
                        <TableRow key={appointment.id}>
                          <TableCell>{appointment.doctorName}</TableCell>
                          <TableCell>{appointment.department}</TableCell>
                          <TableCell>{appointment.date}</TableCell>
                          <TableCell>{appointment.time}</TableCell>
                          <TableCell>
                            <span
                              className={cn(
                                "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                                appointment.status === "Confirmed"
                                  ? "bg-green-100 text-green-800"
                                  : "bg-yellow-100 text-yellow-800"
                              )}
                            >
                              {appointment.status}
                            </span>
                          </TableCell>
                          <TableCell className="text-right">
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() =>
                                handleCancelAppointment(appointment.id)
                              }
                              disabled={appointment.status === "Confirmed"}
                            >
                              Cancel
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                ) : (
                  <div className="text-center py-6">
                    <p className="text-muted-foreground">
                      No appointments scheduled
                    </p>
                    <Button
                      variant="outline"
                      className="mt-4"
                      onClick={() => setIsBookingOpen(true)}
                    >
                      Book Your First Appointment
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="medical-history" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Medical History</CardTitle>
                <CardDescription>
                  View your medical history and records
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-medium">
                      Personal Information
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                      <div className="space-y-1">
                        <p className="text-sm font-medium text-muted-foreground">
                          Full Name
                        </p>
                        <p>{patientInfo.name}</p>
                      </div>
                      <div className="space-y-1">
                        <p className="text-sm font-medium text-muted-foreground">
                          Age
                        </p>
                        <p>{patientInfo.age} years</p>
                      </div>
                      <div className="space-y-1">
                        <p className="text-sm font-medium text-muted-foreground">
                          Blood Group
                        </p>
                        <p>{patientInfo.bloodGroup}</p>
                      </div>
                      <div className="space-y-1">
                        <p className="text-sm font-medium text-muted-foreground">
                          Contact
                        </p>
                        <p>{patientInfo.contact}</p>
                      </div>
                      <div className="space-y-1">
                        <p className="text-sm font-medium text-muted-foreground">
                          Email
                        </p>
                        <p>{patientInfo.email}</p>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium">Medical Conditions</h3>
                    <div className="mt-4 p-4 border rounded-md">
                      <p>
                        {patientInfo.medicalHistory ||
                          "No medical conditions recorded"}
                      </p>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium">Recent Visits</h3>
                    <div className="mt-4">
                      {appointments.length > 0 ? (
                        <div className="space-y-4">
                          {appointments.map((appointment) => (
                            <div
                              key={appointment.id}
                              className="p-4 border rounded-md"
                            >
                              <div className="flex justify-between">
                                <div>
                                  <p className="font-medium">
                                    {appointment.doctorName}
                                  </p>
                                  <p className="text-sm text-muted-foreground">
                                    {appointment.department}
                                  </p>
                                </div>
                                <div className="text-right">
                                  <p>{appointment.date}</p>
                                  <p className="text-sm text-muted-foreground">
                                    {appointment.time}
                                  </p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-muted-foreground">
                          No recent visits recorded
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
