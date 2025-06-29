<template>
  <div id="gallery" class="relative w-full min-w-0 mx-auto mt-10">
    <!-- Carousel wrapper -->
    <div class="relative h-48 sm:h-64 md:h-72 lg:h-[28rem] xl:h-[400px] overflow-hidden rounded-lg">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="absolute w-full h-full transition-opacity duration-700 ease-in-out"
        :class="index === activeIndex ? 'opacity-100' : 'opacity-0'"
      >
        <img
          :src="image.src"
          class="w-full h-full object-cover rounded-lg cursor-pointer"
          :alt="image.label"
          @click="openModal(image.src)"
        />
        <!-- Label Overlay -->
        <div class="absolute bottom-2 right-2 bg-black bg-opacity-60 text-white text-xs sm:text-xl px-2 py-1 rounded">
          {{ image.label }}
        </div>
      </div>
    </div>

    <!-- Slider controls -->
    <button
      @click="prevSlide"
      class="absolute cursor-pointer top-1/2 left-2 transform -translate-y-1/2 z-30 flex items-center justify-center h-9 w-9 sm:h-10 sm:w-10 bg-gray-800/30 rounded-full hover:bg-gray-800/60"
    >
      <svg class="w-4 h-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 1 1 5l4 4" />
      </svg>
    </button>

    <button
      @click="nextSlide"
      class="absolute cursor-pointer top-1/2 right-2 transform -translate-y-1/2 z-30 flex items-center justify-center h-9 w-9 sm:h-10 sm:w-10 bg-gray-800/30 rounded-full hover:bg-gray-800/60"
    >
      <svg class="w-4 h-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 9 4-4-4-4" />
      </svg>
    </button>

    <!-- Fullscreen Image Modal -->
    <div v-if="showModal" @click.self="closeModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80">
      <img :src="modalImage" class="max-w-full max-h-full rounded-lg shadow-lg transition-transform duration-300" />
      <button @click="closeModal" class="absolute top-5 right-5 text-white text-3xl font-bold">&times;</button>
    </div>
  </div>
</template>

<script setup>
  import { ref, defineProps } from 'vue';

  const props = defineProps({
    images: {
      type: Array,
      required: true
    }
  });

  const activeIndex = ref(0);
  const showModal = ref(false);
  const modalImage = ref('');

  const nextSlide = () => {
    activeIndex.value = (activeIndex.value + 1) % props.images.length;
  };

  const prevSlide = () => {
    activeIndex.value = (activeIndex.value - 1 + props.images.length) % props.images.length;
  };

  const openModal = (src) => {
    modalImage.value = src;
    showModal.value = true;
  };

  const closeModal = () => {
    showModal.value = false;
  };
</script>