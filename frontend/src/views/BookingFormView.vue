<template>
  <div class="max-w-4xl mx-auto p-6 mt-27 bg-white rounded shadow-md text-sm">
    <h1 class="text-xl font-bold mb-4 text-center">Reservation Slip</h1>
    <form @submit.prevent="submitForm" class="space-y-4">

      <!-- Header info -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div>
          <label class="font-semibold">Date:</label>
          <input type="date" v-model="form.date" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
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
          <label class="font-semibold">Contact Info:</label>
          <input type="text" v-model="form.contact" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
        <div class="lg:col-span-2">
          <label class="font-semibold">Address:</label>
          <input type="text" v-model="form.address" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
      </div>

      <!-- Dates -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="font-semibold">Inclusive Dates:</label>
          <input type="text" v-model="form.inclusiveDates" class="w-full border border-gray-300 rounded px-2 py-1" />
        </div>
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
                <th class="border px-2 py-1">S</th>
                <th class="border px-2 py-1">D</th>
                <th class="border px-2 py-1">T</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(room, key) in roomTypes" :key="key">
                <td class="border px-2 py-1" v-html="room.label"></td>
                <td class="border px-2 py-1">
                  <input type="number" min="0" v-model.number="form.rooms[key].S" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
                </td>
                <td class="border px-2 py-1">
                  <input type="number" min="0" v-model.number="form.rooms[key].D" class="w-16 border border-gray-300 rounded px-1 py-1 text-center" />
                </td>
                <td class="border px-2 py-1" v-if="room.allowT">
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
        <button type="submit" class="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded">
          Submit Reservation
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue';

const roomTypes = {
  airconPrivate: { label: "<strong>Room A</strong>: Aircon private toilet & bath", allowT: false },
  airconShared: { label: "<strong>Room B</strong>: Aircon shared toilet & bath", allowT: false },
  ceilingFanShared: { label: "<strong>Room C</strong>: Ceiling fan shared toilet & bath", allowT: true },
};

const form = reactive({
  date: '',
  for: '',
  by: '',
  email: '',
  contact: '',
  address: '',
  inclusiveDates: '',
  checkIn: '',
  checkOut: '',
  rooms: {
    airconPrivate: { S: 0, D: 0 },
    airconShared: { S: 0, D: 0 },
    ceilingFanShared: { S: 0, D: 0, T: 0 },
  },
  guests: { F: 0, M: 0 },
});

const totalGuests = computed(() => form.guests.F + form.guests.M);

const submitForm = () => {
  console.log("Submitted form:", form);
  alert("Reservation submitted!");
};
</script>