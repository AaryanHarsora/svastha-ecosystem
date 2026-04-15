const BASE = "http://localhost:8001";

const api = {
    get: async (path) => {
        const res = await fetch(BASE + path);
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
    },
    post: async (path, data) => {
        const res = await fetch(BASE + path, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Error"); }
        return res.json();
    },
    put: async (path, data) => {
        const res = await fetch(BASE + path, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Error"); }
        return res.json();
    },
    delete: async (path) => {
        const res = await fetch(BASE + path, { method: "DELETE" });
        if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Error"); }
        return res.json();
    },

    // Patients
    patients: () => api.get("/patients/"),
    patientRisk: (id) => api.get(`/patients/${id}/risk`),
    patientAppointments: (id) => api.get(`/patients/${id}/appointments`),
    patientSymptoms: (id) => api.get(`/patients/${id}/symptoms`),
    patientOrders: (id) => api.get(`/patients/${id}/orders`),
    highRiskPatients: (t = 70) => api.get(`/patients/high-risk/list?threshold=${t}`),
    noDisease: () => api.get("/patients/no-disease/list"),
    createPatient: (data) => api.post("/patients/", data),
    updatePatient: (id, data) => api.put(`/patients/${id}`, data),
    deletePatient: (id) => api.delete(`/patients/${id}`),
    addSymptom: (id, symptom_id) => api.post(`/patients/${id}/symptoms`, { symptom_id }),
    submitHealth: (id, data) => api.post(`/patients/${id}/health`, data),

    // Diseases & Symptoms
    diseases: () => api.get("/diseases/"),
    diseasePatientCount: () => api.get("/diseases/patient-count"),
    symptoms: () => api.get("/diseases/symptoms"),

    // Appointments
    appointments: () => api.get("/appointments/"),
    doctors: () => api.get("/appointments/doctors"),
    hospitals: () => api.get("/appointments/hospitals"),
    createAppointment: (data) => api.post("/appointments/", data),
    updateAppointment: (id, data) => api.put(`/appointments/${id}`, data),
    deleteAppointment: (id) => api.delete(`/appointments/${id}`),

    // Medications
    medications: () => api.get("/medications/"),
    topSelling: (n = 5) => api.get(`/medications/top-selling?limit=${n}`),
    cheapestPerCategory: () => api.get("/medications/cheapest-per-category"),
    createMedication: (data) => api.post("/medications/", data),
    updateMedication: (id, data) => api.put(`/medications/${id}`, data),
    deleteMedication: (id) => api.delete(`/medications/${id}`),

    // Marketplace
    inventory: () => api.get("/marketplace/inventory"),
    stock: () => api.get("/marketplace/stock"),
    vendors: () => api.get("/marketplace/vendors"),
    ordersSummary: () => api.get("/marketplace/orders/summary"),
    ordersPerPatient: () => api.get("/marketplace/orders/per-patient"),
    createOrder: (data) => api.post("/marketplace/orders", data),
    updateOrderStatus: (id, status) => api.put(`/marketplace/orders/${id}/status`, { status }),
    cancelOrder: (id) => api.delete(`/marketplace/orders/${id}`),
    updateInventory: (id, data) => api.put(`/marketplace/inventory/${id}`, data),

    // Recommendations
    recommendations: (id) => api.get(`/recommendations/${id}`),
};