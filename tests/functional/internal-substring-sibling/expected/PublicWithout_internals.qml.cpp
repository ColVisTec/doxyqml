namespace demo {
/**
 * A class with a funny name
 */
/** \n <br><b>Import Statement</b> \n @code import demo @endcode */
/** @version 1.0 */
class PublicWithout_internals : public QtQml.QtObject {
public:
/**
 * Some normal property
 */
Q_PROPERTY(int foo READ dummyGetter_foo_ignore)
};
}
