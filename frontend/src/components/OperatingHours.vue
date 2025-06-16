<template>
  <div class="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg z-10">
    <h2 class="text-2xl font-bold text-center mb-6">Operating Hours</h2>
    <div class="overflow-x-auto">
      <table class="w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-[#09240B] text-white">
            <th class="p-4 text-left">Description</th>
            <th class="p-4 text-left">Time</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border border-gray-300">
            <td class="p-3 font-medium text-gray-800">Hours</td>
            <td class="p-3 text-gray-700">5:00 a.m. – 11:00 p.m.</td>
          </tr>
          <tr class="border border-gray-300">
            <td class="p-3 font-medium text-gray-800">Curfew</td>
            <td class="p-3 text-gray-700">11:00 p.m. – 5:00 a.m.</td>
          </tr>
          <tr class="border border-gray-300">
            <td class="p-3 font-medium text-gray-800">Check-in</td>
            <td class="p-3 text-gray-700">2:00 p.m.</td>
          </tr>
          <tr class="border border-gray-300">
            <td class="p-3 font-medium text-gray-800">Check-out</td>
            <td class="p-3 text-gray-700">12:00 noon</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
// no script needed unless you're fetching data
</script>
