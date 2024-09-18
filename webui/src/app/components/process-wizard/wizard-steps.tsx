interface WizardStepsProps {
    steps: string[]
    currentStep: number
  }
  
  export default function WizardSteps({ steps, currentStep }: WizardStepsProps) {
    return (
      <div className="flex justify-between items-center">
        {steps.map((step, index) => (
          <div key={step} className="flex items-center">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center ${
                index <= currentStep ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}
            >
              {index + 1}
            </div>
            <div className="ml-2 text-sm font-medium">{step}</div>
            {index < steps.length - 1 && (
              <div
                className={`h-0.5 w-full mx-2 ${
                  index < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              />
            )}
          </div>
        ))}
      </div>
    )
  }