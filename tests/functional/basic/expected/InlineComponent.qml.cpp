using namespace QtQuick;
/// This item conteins an inline component and a Component
class InlineComponent : public QtQuick.Item {
public:
/// This is inline component example
class ThisIsInlineComponent : public Text {
public:
/// This is inline component property 
Q_PROPERTY(string someProperty READ dummyGetter_someProperty_ignore)
};
/// This is a component example 
Q_PROPERTY(Component thisIsAComponent READ dummyGetter_thisIsAComponent_ignore)
private:
/// This is a column
Column col;
};
