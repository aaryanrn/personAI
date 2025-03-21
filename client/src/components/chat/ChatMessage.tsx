type ChatMessageProps = {
  message: string;
  accentColor: string;
  name: string;
  isSelf: boolean;
  hideName?: boolean;
};

export const ChatMessage = ({
  name,
  message,
  accentColor,
  isSelf,
  hideName,
}: ChatMessageProps) => {
  // accentColor="blue"
  return (
    <div className={`flex flex-col gap-1 ${hideName ? "pt-0" : "pt-6"}`}>
      {!hideName && (
        <div
          className={` font-bold text-lg text-${
            isSelf ? "gray-800" : accentColor + "-900 text-ts-" + accentColor
          } uppercase text-xs`}
        >
          {name}
        </div>
      )}
      <div
        className={`pr-4 text-${isSelf ? "stone-500" : accentColor + "-700"} text-sm ${
          isSelf ? "" : `drop-shadow-[0_1px_2px_rgba(${accentColor},0.3)]`
        } whitespace-pre-line`}
      >
        {message}
      </div>
    </div>
  );
};
