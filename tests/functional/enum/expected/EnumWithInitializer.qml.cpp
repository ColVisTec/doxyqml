class EnumWithInitializer : public QtQuick.Item {
public:
enum class MyEnum {
/// The first
First = 1,
InBetween,
Last = MyConstant ///< The last
};
};
