<template>
  <div class="max-w-4xl mx-auto p-6 mt-27 bg-white rounded shadow-md text-sm">
    <h1 class="text-xl font-bold mb-4 text-center">Reservation Slip</h1>
    <form @submit.prevent="submitForm" class="space-y-4">

      <!-- Header info -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div>
          <label class="font-semibold">For (Person/Company/Unit):</label>
          <input type="text" v-model="form.for" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
        <div>
          <label class="font-semibold">By (Contact Person/Address):</label>
          <input type="text" v-model="form.by" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
        <div>
          <label class="font-semibold">Email:</label>
          <input type="email" v-model="form.email" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
        <div>
          <label class="font-semibold">Phone Number:</label>
          <input type="text" v-model="form.contact" placeholder="09XX XXX XXXX" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
        <div class="lg:col-span-2">
          <label class="font-semibold">Address:</label>
          <input type="text" v-model="form.address" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
      </div>

      <!-- Dates -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div>
          <label class="font-semibold">Check-in:</label>
          <input type="date" v-model="form.checkIn" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
        <div>
          <label class="font-semibold">Check-out:</label>
          <input type="date" v-model="form.checkOut" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
      </div>

      <!-- Rooms Table -->
      <div>
        <label class="block font-semibold mb-2">No. of Rooms</label>
        <div class="overflow-x-auto">
          <table class="w-full table-auto border border-gray-300">
            <thead class="bg-gray-100">
              <tr>
                <th class="border px-2 py-1">Room Type</th>
                <th class="border px-2 py-1">Single<br><span style="font-weight: normal !important;">(1 Pax)</span></th>
                <th class="border px-2 py-1">Double<br><span style="font-weight: normal !important;">(2 Pax)</span></th>
                <th class="border px-2 py-1">Triple<br><span style="font-weight: normal !important;">(3 Pax)</span></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(room, key) in roomTypes" :key="key">
                <td class="border px-2 py-1" v-html="room.label"></td>
                <td class="border px-2 py-1 text-center">
                  <input type="number" min="0" v-model.number="form.rooms[key].S" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
                </td>
                <td class="border px-2 py-1 text-center">
                  <input type="number" min="0" v-model.number="form.rooms[key].D" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
                </td>
                <td class="border px-2 py-1 text-center" v-if="room.allowT">
                  <input type="number" min="0" v-model.number="form.rooms[key].T" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
                </td>
                <td class="border px-2 py-1" v-else></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Guest Count -->
      <div>
        <label class="font-semibold block">No. of Guests</label>
        <div class="flex gap-4">
          <div><label><strong>F</strong>: </label>
            <input type="number" min="0" v-model.number="form.guests.F" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
          </div>
          <div><label><strong>M</strong>: </label>
            <input type="number" min="0" v-model.number="form.guests.M" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
          </div>
          <div><label><strong>All</strong>: </label>
            <span class="inline-block px-1 py-1 text-center">{{ totalGuests }}</span>
          </div>
        </div>
      </div>

      <!-- Guest Information -->
      <div v-if="totalGuests > 0" class="mt-6">
        <h2 class="font-semibold mb-2">Guest Information ({{ totalGuests }})</h2>

        <!-- Grid of guest cards: 1 column on small screens, 2 columns on md and up -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="(guest, index) in form.guestDetails" :key="index" class="p-4 border rounded">
            <label class="block font-semibold mb-1">Guest #{{ index + 1 }} Name</label>
            <input v-model="guest.name" type="text" class="w-full border border-gray-300 rounded px-2 py-1 mb-2" />

            <label class="block font-semibold mb-1">Age Range</label>
            <select v-model="guest.ageRange" class="w-full border border-gray-300 rounded px-2 py-1">
              <option disabled value="">Select age range</option>
              <option value="13-17">13 to 17</option>
              <option value="18+">18 years and above</option>
            </select>
          </div>
        </div>
      </div>


      <!-- Reminders -->
      <div class="mt-6 p-4 border rounded bg-gray-50">
        <h2 class="font-semibold mb-2">Reminders:</h2>
        <ul class="list-disc pl-5 space-y-1">
          <li>Please confirm your registration at least one week before check-in date.</li>
          <li>Any changes in reservation should be made 48 hours in advance.</li>
          <li>The hostel closes at 11 PM and opens at 5 AM. Check-in is 2 PM, check-out is 12 noon.</li>
          <li>Present your ID card when you register/check in.</li>
        </ul>
      </div>

      <!-- Submit Button -->
      <div class="text-right">
        <button type="submit" class="cursor-pointer bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded">
          Submit Reservation
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
  import { reactive, computed, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useToast } from 'vue-toastification'

  const router = useRouter()
  const toast = useToast()

  const roomTypes = {
    airconPrivate: { label: "<strong>Room A</strong>: Aircon private toilet & bath", allowT: false },
    airconShared: { label: "<strong>Room B</strong>: Aircon shared toilet & bath", allowT: false },
    ceilingFanShared: { label: "<strong>Room C</strong>: Ceiling fan shared toilet & bath", allowT: true },
  }

  const form = reactive({
    date: '',
    for: '',
    by: '',
    email: '',
    contact: '',
    address: '',
    checkIn: '',
    checkOut: '',
    rooms: {
      airconPrivate: { S: 0, D: 0 },
      airconShared: { S: 0, D: 0 },
      ceilingFanShared: { S: 0, D: 0, T: 0 },
    },
    guests: { F: 0, M: 0 },
    guestDetails: [],
  })

  const totalGuests = computed(() => form.guests.F + form.guests.M)

  watch(totalGuests, (newCount) => {
    const current = form.guestDetails.length
    if (newCount > current) {
      for (let i = current; i < newCount; i++) {
        form.guestDetails.push({ name: '', ageRange: '' })
      }
    } else if (newCount < current) {
      form.guestDetails.splice(newCount)
    }
  })

  const submitForm = async () => {
    const requiredFields = {
      "For (Person/Company/Unit)": form.for,
      "By (Contact Person/Address)": form.by,
      "Email": form.email,
      "Phone Number (09XX XXX XXXX)": form.contact,
      "Address": form.address,
      "Check-in": form.checkIn,
      "Check-out": form.checkOut,
    }

    const missingFields = Object.entries(requiredFields)
      .filter(([_, value]) => !value || value.toString().trim() === "")
      .map(([label]) => label)

    if (missingFields.length > 0) {
      toast.warning(`Please fill in the following fields:\n\n${missingFields.join('\n')}`)
      return
    }

    const roomCounts = [
      form.rooms.airconPrivate.S, form.rooms.airconPrivate.D,
      form.rooms.airconShared.S, form.rooms.airconShared.D,
      form.rooms.ceilingFanShared.S, form.rooms.ceilingFanShared.D, form.rooms.ceilingFanShared.T
    ]
    const hasRoom = roomCounts.some(count => count > 0)

    if (!hasRoom) {
      toast.warning("Please select at least one room.")
      return
    }

    if (form.guests.M <= 0 && form.guests.F <= 0) {
      toast.warning("Please enter at least one male or female guest.")
      return
    }

    const phoneRegex = /^09\d{2} \d{3} \d{4}$/
    if (!phoneRegex.test(form.contact)) {
      toast.warning("Please enter a valid phone number in the format:\n09XX XXX XXXX")
      return
    }

    const start = new Date(form.checkIn)
    const end = new Date(form.checkOut)
    const diffInDays = (end - start) / (1000 * 3600 * 24)

    if (diffInDays > 14) {
      toast.warning("Reservation cannot exceed 14 days. Please shorten the stay.")
      return
    }

    for (let i = 0; i < totalGuests.value; i++) {
      const guest = form.guestDetails[i]
      if (!guest.name || !guest.ageRange) {
        toast.warning(`Please complete Guest #${i + 1} information.`)
        return
      }
    }

    const payload = {
      guest_name: form.by,
      guest_email: form.email,
      phone_number: form.contact,
      address: form.address,
      start_date: form.checkIn,
      end_date: form.checkOut,
      for_person_name: form.for,
      male_count: form.guests.M,
      female_count: form.guests.F,
      single_a_room_count: form.rooms.airconPrivate.S,
      double_a_room_count: form.rooms.airconPrivate.D,
      single_b_room_count: form.rooms.airconShared.S,
      double_b_room_count: form.rooms.airconShared.D,
      single_c_room_count: form.rooms.ceilingFanShared.S,
      double_c_room_count: form.rooms.ceilingFanShared.D,
      triple_c_room_count: form.rooms.ceilingFanShared.T,
      guest_details: form.guestDetails,
    }

    const loadingToastId = toast.info("Sending reservation...", { timeout: false })

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_BASE_URL
      const res = await fetch(`${backendUrl}/reserve/create_new_reservation/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })

      let data = {}
      try {
        data = await res.json()
      } catch {
        toast.dismiss(loadingToastId)
        toast.error("Invalid response from server.")
        return
      }

      if (!res.ok || !data.reservation_token) {
        toast.dismiss(loadingToastId)
        const errorMessages = data?.error || Object.entries(data)
          .map(([field, messages]) => `${field.replace('_', ' ')}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('\n')
        toast.error(`Reservation failed:\n\n${errorMessages}`)
        return
      }

      toast.dismiss(loadingToastId)
      toast.success("Verification email sent! Redirecting to verification page...")
      router.push({ name: 'verify', query: { token: data.reservation_token } })

    } catch (err) {
      toast.dismiss(loadingToastId)
      console.error("Network error:", err)
      toast.error("Network error: could not submit reservation.")
    }
  }
</script>