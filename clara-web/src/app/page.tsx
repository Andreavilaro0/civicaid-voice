export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 text-center">
      <h1 className="font-display text-h1 font-bold text-clara-blue mb-4">
        Clara
      </h1>
      <p className="font-display text-h2 text-clara-text mb-6">
        Tu voz tiene poder
      </p>
      <p className="text-body text-clara-text-secondary max-w-md">
        Asistente de voz que te ayuda con tramites sociales en Espana.
        Habla o escribe en tu idioma.
      </p>
      <div className="mt-8 flex gap-4">
        <div className="w-4 h-4 rounded-full bg-clara-blue" />
        <div className="w-4 h-4 rounded-full bg-clara-orange" />
        <div className="w-4 h-4 rounded-full bg-clara-green" />
      </div>
      <p className="mt-8 text-label text-clara-text-secondary">
        Scaffolding completo — Q3 agregara los componentes.
      </p>
    </div>
  );
}
